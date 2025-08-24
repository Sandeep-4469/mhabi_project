import streamlit as st
import pandas as pd
from src.data_loader import validate_uploaded_csv, load_initial_data

st.set_page_config(page_title="Upload Data", layout="wide")

st.title("Upload New Patient Data")
st.markdown("Upload a CSV file to add new patient records to the current dataset in this session.")
st.info("The operation will be cancelled if any `patient_id` in your uploaded file already exists in the current dataset.")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type="csv"
)

if uploaded_file is not None:
    df, error = validate_uploaded_csv(uploaded_file)
    if error:
        st.error(error)
    else:
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        if st.button(f"Append {len(df)} Records to Dashboard"):
            existing_data = st.session_state.data
            
            existing_ids = set(existing_data['patient_id'])
            upload_ids = set(df['patient_id'])
            duplicates = existing_ids.intersection(upload_ids)
            
            if duplicates:
                st.error(f"Cannot append. The following patient_id values already exist: **{', '.join(map(str, duplicates))}**")
            else:
                combined_df = pd.concat([existing_data, df], ignore_index=True)
                st.session_state.data = combined_df
                st.success(f"Successfully appended {len(df)} records. The dashboard now contains **{len(combined_df)}** total records.")
                st.info("Navigate to the 'Dashboard' page to see the updated analysis.")

st.divider()
st.subheader("Reset to Default Data")
st.markdown("If you want to return to the original sample dataset, click the button below.")
if st.button("Reset to Sample Data"):
    st.session_state.data = load_initial_data()
    st.success("Dataset has been reset to the default sample data.")
