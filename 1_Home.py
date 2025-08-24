import streamlit as st
from src.data_loader import load_initial_data
from src.mhabi_algorithm import calculate_mhabi

st.set_page_config(page_title="MHABI Home", layout="wide")

# Initialize session state if it doesn't exist
if 'data' not in st.session_state:
    st.session_state.data = load_initial_data()

st.title("Welcome to the Mental Health Acute Burden Index (MHABI) Dashboard")
st.markdown("---")

# --- NEW: Quick Calculator Section ---
with st.expander("Quick Score Calculator", expanded=False):
    st.markdown("Enter a patient's details below to get an immediate MHABI score. This calculation will not be saved.")
    
    with st.form("calculator_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            wait_time_days = st.number_input("Wait Time (days)", min_value=0, step=1)
            dalys = st.number_input("DALYs Score", min_value=0.0, format="%.2f", step=0.01)
        with col2:
            er_visits_last_year = st.number_input("ER Visits (last year)", min_value=0, step=1)
            missed_work_school_days = st.number_input("Missed Work/School (days)", min_value=0, step=1)
        with col3:
            suicide_risk_score = st.slider("Suicide Risk Score", min_value=1, max_value=10, value=5)
        
        submitted = st.form_submit_button("Calculate Score")

    if submitted:
        # Create a dictionary from the inputs
        patient_inputs = {
            'wait_time_days': wait_time_days,
            'dalys': dalys,
            'er_visits_last_year': er_visits_last_year,
            'missed_work_school_days': missed_work_school_days,
            'suicide_risk_score': suicide_risk_score
        }
        # Run the calculation
        result = calculate_mhabi(patient_inputs)
        
        st.subheader("Calculation Result")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="MHABI Score", value=f"{result['mhabi_score']:.2f}")
        with res_col2:
            if result['risk_amplified']:
                st.warning("Risk Status: Amplified")
            else:
                st.success("Risk Status: Not Amplified")

st.header("Project Overview")
st.markdown("This tool is a proof-of-concept for the **Mental Health Acute Burden Index (MHABI)**, a composite score designed to quantify the severity of a patient's mental health burden for prioritization and resource allocation. It combines multiple factors into a single, understandable metric.")
st.header("How to Use This Tool")
st.info("1.  **Use the Calculator:** Quickly assess a single patient using the form above.\n2.  **Upload Your Data:** Navigate to the **Upload Data** page to load a full CSV file for batch analysis.\n3.  **Explore the Dashboard:** Go to the **Dashboard** page to analyze the loaded dataset.")
