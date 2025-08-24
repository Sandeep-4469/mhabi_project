import streamlit as st
import pandas as pd
import plotly.express as px
from src.mhabi_algorithm import process_dataframe

st.set_page_config(page_title="MHABI Dashboard", layout="wide")

st.title("Interactive MHABI Dashboard")

if 'data' not in st.session_state or st.session_state.data.empty:
    st.warning("No data loaded. Please go to the 'Upload Data' page to load a CSV file.")
    st.stop()

current_data = st.session_state.data
processed_data = process_dataframe(current_data)

st.sidebar.header("Filter Options")
regions = sorted(processed_data['region'].unique())
selected_regions = st.sidebar.multiselect("Select Region(s)", options=regions, default=regions)
age_groups = sorted(processed_data['age_group'].unique())
selected_age_groups = st.sidebar.multiselect("Select Age Group(s)", options=age_groups, default=age_groups)
genders = sorted(processed_data['gender'].unique())
selected_genders = st.sidebar.multiselect("Select Gender(s)", options=genders, default=genders)

filtered_df = processed_data[
    (processed_data['region'].isin(selected_regions)) &
    (processed_data['age_group'].isin(selected_age_groups)) &
    (processed_data['gender'].isin(selected_genders))
]

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
else:
    st.header("Exploratory Analysis")
    plot_options = [
        "MHABI Score Distribution",
        "Average Score by Region",
        "Score Distribution by Age Group",
        "Wait Time vs. MHABI Score",
        "Key Statistics Summary"
    ]
    selected_plot = st.selectbox("Choose a visualization:", plot_options)

    # --- ALL PLOTS VERIFIED AND WORKING ---
    if selected_plot == "MHABI Score Distribution":
        fig = px.histogram(filtered_df, x='mhabi_score', nbins=20, title="Distribution of MHABI Scores", marginal="box", color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig, use_container_width=True)

    elif selected_plot == "Average Score by Region":
        avg_scores = filtered_df.groupby('region')['mhabi_score'].mean().reset_index()
        fig = px.bar(avg_scores, x='region', y='mhabi_score', title="Average MHABI Score by Region", color='region', labels={'mhabi_score': 'Average MHABI Score'})
        st.plotly_chart(fig, use_container_width=True)
        
    elif selected_plot == "Score Distribution by Age Group":
        # Sort age groups for proper order in the plot
        age_order = sorted(filtered_df['age_group'].unique())
        fig = px.box(filtered_df, x='age_group', y='mhabi_score', title="MHABI Score Distribution by Age Group", color='age_group', category_orders={'age_group': age_order}, labels={'mhabi_score': 'MHABI Score', 'age_group': 'Age Group'})
        st.plotly_chart(fig, use_container_width=True)

    elif selected_plot == "Wait Time vs. MHABI Score":
        fig = px.scatter(filtered_df, x='wait_time_days', y='mhabi_score', color='region', title="Wait Time vs. MHABI Score", trendline="ols", trendline_color_override="red", labels={'wait_time_days': 'Wait Time (Days)', 'mhabi_score': 'MHABI Score'})
        st.plotly_chart(fig, use_container_width=True)

    elif selected_plot == "Key Statistics Summary":
        st.subheader("Summary of Numerical Data")
        st.dataframe(filtered_df[['wait_time_days', 'dalys', 'er_visits_last_year', 'missed_work_school_days', 'suicide_risk_score', 'mhabi_score']].describe())
    
    st.header("Patient-Level Data")
    st.info(f"Displaying {len(filtered_df)} of {len(current_data)} total records.")
    def highlight_amplified(row):
        style = 'background-color: #ffcccc; color: black;'
        return [style for _ in row] if row.risk_amplified else ['' for _ in row]
    
    display_cols = ['patient_id', 'region', 'age_group', 'gender', 'mhabi_score', 'risk_amplified']
    st.dataframe(filtered_df[display_cols].style.apply(highlight_amplified, axis=1), use_container_width=True)
