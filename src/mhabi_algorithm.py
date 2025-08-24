import pandas as pd
def _normalize_wait_time(days):
    if days <= 7: return 10
    if days <= 30: return 40
    if days <= 90: return 70
    return 100
def _normalize_dalys(daly_score):
    if daly_score < 0.1: return 10
    if daly_score < 0.2: return 40
    if daly_score < 0.3: return 70
    return 100
def _normalize_er_visits(visits):
    if visits == 0: return 0
    if visits == 1: return 40
    if visits == 2: return 70
    return 100
def _normalize_missed_work(days):
    if days <= 5: return 10
    if days <= 10: return 40
    if days <= 20: return 70
    return 100
def _normalize_suicide_risk(risk_score):
    if risk_score <= 3: return 10
    if risk_score <= 6: return 50
    if risk_score <= 8: return 80
    return 100
def calculate_mhabi(patient_data_row):
    raw_suicide_risk = patient_data_row['suicide_risk_score']
    norm_scores = {"Wait Time": _normalize_wait_time(patient_data_row['wait_time_days']), "DALYs/YLDs": _normalize_dalys(patient_data_row['dalys']), "ER Utilization": _normalize_er_visits(patient_data_row['er_visits_last_year']), "Missed Work/School": _normalize_missed_work(patient_data_row['missed_work_school_days']), "Suicide Risk": _normalize_suicide_risk(raw_suicide_risk)}
    weights = {"Wait Time": 0.25, "DALYs/YLDs": 0.20, "ER Utilization": 0.20, "Missed Work/School": 0.15, "Suicide Risk": 0.20}
    subtotal = sum(norm_scores[key] * weights[key] for key in norm_scores)
    amplified = False
    final_score = subtotal
    if raw_suicide_risk >= 7 and patient_data_row['er_visits_last_year'] >= 2:
        final_score *= 1.1
        amplified = True
    return {"mhabi_score": round(min(final_score, 100), 2), "normalized_scores": norm_scores, "risk_amplified": amplified}

def process_dataframe(df):
    if df.empty: return df
    results = df.apply(calculate_mhabi, axis=1)
    processed_df = df.copy()
    processed_df['mhabi_score'] = results.apply(lambda x: x['mhabi_score'])
    processed_df['risk_amplified'] = results.apply(lambda x: x['risk_amplified'])
    processed_df['normalized_scores'] = results.apply(lambda x: x['normalized_scores'])
    return processed_df
