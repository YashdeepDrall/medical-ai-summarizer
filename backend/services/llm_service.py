import google.generativeai as genai
from backend.config import GEMINI_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Use Gemini 3.1 Flash Lite
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")


def generate_summary(patient_data, knowledge_chunks):

    knowledge_text = "\n".join(knowledge_chunks)

    prompt = f"""
You are a medical report summarizer AI.

Your task:
Summarize patient biomarker data using medical knowledge.

IMPORTANT RULES:
- Do not give medical diagnosis
- Only provide interpretation
- Use simple language
- Group biomarkers by category

Patient Biomarker Data:
{patient_data}

Relevant Medical Knowledge:
{knowledge_text}

Output format:

Patient Health Summary

Category:
- Biomarker: value (status)

Key Observations:
- bullet points

Health Risk Indicators:
- bullet points

Disclaimer:
This AI summary is for informational purposes only.
"""

    response = model.generate_content(prompt)

    return response.text