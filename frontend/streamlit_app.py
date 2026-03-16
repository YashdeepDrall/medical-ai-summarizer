import sys
import os

# Fix backend import issue
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import requests
from backend.services.parser import parse_pdf_report, extract_text_from_pdf, clean_pdf_text

API_URL = "http://127.0.0.1:8000/summarize-report"

st.set_page_config(page_title="Medical AI Summarizer")
st.title("🩺 AI Medical Report Summarizer")
st.write("Upload a patient report (CSV or PDF) to generate AI summary.")

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader(
    "Upload Patient Report",
    type=["csv", "pdf"]
)

# -------------------------------
# CSV Parser
# -------------------------------
def parse_csv(file):
    df = pd.read_csv(file)
    return df

# -------------------------------
# Main Processing
# -------------------------------
if uploaded_file:

    file_type = uploaded_file.name.split(".")[-1].lower()
    report_data = []

    # ---------------- CSV Upload ----------------
    if file_type == "csv":
        df = parse_csv(uploaded_file)
        st.subheader("📊 Report Preview")
        st.dataframe(df)
        report_data = df.to_dict(orient="records")

    # ---------------- PDF Upload ----------------
    elif file_type == "pdf":
        pdf_text = extract_text_from_pdf(uploaded_file)
        pdf_text = clean_pdf_text(pdf_text)
        report_data = parse_pdf_report(uploaded_file)

        if len(report_data) == 0:
            st.error("No biomarkers detected in PDF. Please check PDF format.")
            st.write("PDF Text Preview:")
            st.text(pdf_text[:1000])
        else:
            df = pd.DataFrame(report_data)
            st.subheader("🧬 Extracted Biomarkers")
            st.dataframe(df)

    # ---------------- Generate AI Summary ----------------
    if st.button("Generate AI Summary"):

        if len(report_data) == 0:
            st.error("No biomarker data available to generate summary.")
        else:
            # Ensure all Values are floats
            for r in report_data:
                try:
                    r["Value"] = float(r["Value"])
                except:
                    r["Value"] = 0.0

            with st.spinner("Analyzing report with AI..."):
                try:
                    response = requests.post(
                        API_URL,
                        json=report_data
                    )

                    if response.status_code == 200:
                        result = response.json()
                        st.subheader("🧪 Biomarker Analysis")
                        st.dataframe(pd.DataFrame(result["biomarker_analysis"]))

                        st.subheader("🧠 AI Health Summary")
                        st.write(result["ai_summary"])

                    else:
                        st.error(f"Error connecting to backend API: {response.status_code}")

                except Exception as e:
                    st.error(f"API request failed: {e}")