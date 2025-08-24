import pandas as pd
import streamlit as st

def load_initial_data(file_path='data/sample_emr_data.csv'):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Initial data file not found at {file_path}")
        return pd.DataFrame()

def validate_uploaded_csv(uploaded_file):
    required_columns = [
        'patient_id', 'region', 'age_group', 'gender', 'wait_time_days',
        'dalys', 'er_visits_last_year', 'missed_work_school_days', 'suicide_risk_score'
    ]
    try:
        df = pd.read_csv(uploaded_file)
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            error_message = f"Validation Error: The CSV is missing required columns: **{', '.join(missing_cols)}**"
            return None, error_message
        return df, None
    except Exception as e:
        return None, f"An error occurred while reading the file: {e}"
