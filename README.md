# Mental Health Acute Burden Index (MHABI) Dashboard

This interactive web application is a tool for researchers, clinicians, and public health officials to calculate, visualize, and analyze the Mental Health Acute Burden Index (MHABI) score for patient populations. It is designed to be user-friendly, allowing for both quick single-patient assessments and in-depth analysis of larger datasets.

---

## How to Run the Application Locally

To run this application on your own computer, follow these steps.

**1. Prerequisites:**
*   You must have Python 3.8 or newer installed.

**2. Setup:**
*   Download or clone this repository to your computer.
*   Open a terminal or command prompt and navigate into the project folder (`mhabi-dashboard`).

**3. Create a Virtual Environment (Recommended):**
```bash
# For MacOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

**4. Install Required Packages:**
```bash
pip install -r requirements.txt
```

**5. Run the Application:**
```bash
streamlit run 1_Home.py
```
Your web browser will automatically open with the application running.

---

## User Guide: How to Use the Application

This application is organized into four main pages, which you can select from the sidebar on the left.

### 1. Home Page

This is the landing page of the application.

*   **Purpose:** To welcome you to the tool, explain what the MHABI score is, and provide a quick way to calculate a score for a single patient.
*   **How to Use:**
    *   Read the **Project Overview** to understand the goal of the MHABI score.
    *   To test the algorithm, expand the **"Quick Score Calculator"** section.
    *   Enter the metrics for a single patient into the form fields.
    *   Click the **"Calculate Score"** button.
    *   The calculated **MHABI Score** and the patient's **Risk Status** will appear instantly below the form.
    *   **Note:** This calculator is for quick, one-off assessments. The data you enter here is **not** saved or added to the main dashboard dataset.

### 2. Dashboard Page

This is the main analysis page where you can explore the loaded dataset.

*   **Purpose:** To visualize the MHABI scores of the entire patient population currently loaded in your session.
*   **How to Use:**
    *   **Filter Your Data:** Use the **"Filter Options"** in the sidebar on the left to narrow down the dataset by region, age group, or gender. The charts will update automatically.
    *   **Choose a Visualization:** Select a graph from the dropdown menu to explore the data in different ways (e.g., see the overall score distribution, compare average scores between regions, etc.).
    *   **View Detailed Data:** The table at the bottom of the page shows the raw data for your filtered selection. Patients with a high-risk profile (whose scores were amplified) will be **highlighted in red** for easy identification.

### 3. Upload Data Page

This page allows you to load your own patient data for analysis.

*   **Purpose:** To load, append, or reset the dataset that is used on the Dashboard page.
*   **How to Use:**
    1.  Click the **"Browse files"** button and select a CSV file from your computer. (See "Data Format Requirements" below).
    2.  The application will show a preview of your uploaded data.
    3.  **To add your data to the existing set**, turn **ON** the **"Append to existing data"** toggle. The app will check for duplicate patient IDs and will only add new, unique records.
    4.  **To replace the existing data** with your new file, leave the toggle **OFF**.
    5.  Click the button (e.g., "Append 7 records...") to load the data into your session.
    6.  **To start over**, you can click the **"Reset to Sample Data"** button at any time to clear all uploaded data and return to the original sample dataset.

### 4. Data Dictionary Page

This page provides clear definitions for each data field used in the calculation.

*   **Purpose:** To help you understand what each data attribute means and why it is important for the MHABI score.
*   **How to Use:**
    *   Simply click on any attribute name (e.g., `wait_time_days` or `dalys`).
    *   The section will expand to show a detailed definition and its significance in the algorithm.

---

## Data Format Requirements

When preparing a CSV file for upload, please ensure it contains the following **nine columns** with the exact names listed below. All columns are required for the calculation to work correctly.

| Column Name                 | Data Type       | Example     | Description                                               |
| --------------------------- | --------------- | ----------- | --------------------------------------------------------- |
| `patient_id`                | Text or Number  | `P101`      | A unique ID for the patient.                              |
| `region`                    | Text            | `North`     | The patient's geographical region.                        |
| `age_group`                 | Text            | `25-34`     | The patient's age bracket.                                |
| `gender`                    | Text            | `Female`    | The patient's gender.                                     |
| `wait_time_days`            | Number          | `90`        | Days the patient has been on a waitlist.                  |
| `dalys`                     | Decimal Number  | `0.25`      | Disability-Adjusted Life Years score.                     |
| `er_visits_last_year`       | Number          | `2`         | Number of mental health-related ER visits in the past year. |
| `missed_work_school_days`   | Number          | `20`        | Days of work/school missed in the past 3 months.          |
| `suicide_risk_score`        | Number (1-10)   | `8`         | A clinically assessed suicide risk score from 1 to 10.    |