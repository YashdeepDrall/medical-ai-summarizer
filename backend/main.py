from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
from backend.config import GEMINI_API_KEY

# -------------------------------
# Configure Gemini AI
# -------------------------------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

# -------------------------------
# FastAPI App
# -------------------------------
app = FastAPI()

# Allow Streamlit / Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Pydantic Model
# -------------------------------
class Biomarker(BaseModel):
    Biomarker: str
    Value: float
    Unit: Optional[str] = None
    Reference_Range: Optional[str] = None

# -------------------------------
# Helper: AI Summary Generation
# -------------------------------
def generate_ai_summary(biomarkers: List[Biomarker]):
    # Build knowledge text
    knowledge_chunks = []  # In future: load from PDFs in `data/` folder
    knowledge_text = "\n".join(knowledge_chunks)

    # Build patient biomarker text
    patient_text = ""
    for b in biomarkers:
        patient_text += f"{b.Biomarker}: {b.Value} {b.Unit or ''} (Ref: {b.Reference_Range})\n"

    prompt = f"""
You are a medical report summarizer AI.

Task:
- Summarize patient biomarker data using medical knowledge.
- Do not give diagnosis, only interpretation.
- Group biomarkers by category.

Patient Biomarker Data:
{patient_text}

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


# -------------------------------
# Summarize Endpoint
# -------------------------------
@app.post("/summarize-report")
async def summarize_report(biomarkers: List[Biomarker]):
    analysis = []

    # Simple Normal/Low/High check based on Reference_Range
    for b in biomarkers:
        status = "Normal"
        try:
            if b.Reference_Range:
                parts = b.Reference_Range.replace(">", "").replace("<", "").split("-")
                if len(parts) == 2:
                    low = float(parts[0].strip())
                    high = float(parts[1].strip())
                    if b.Value < low:
                        status = "Low"
                    elif b.Value > high:
                        status = "High"
        except:
            status = "Unknown"

        analysis.append({
            "Biomarker": b.Biomarker,
            "Value": b.Value,
            "Unit": b.Unit,
            "Reference_Range": b.Reference_Range,
            "Status": status
        })

    # AI Summary
    ai_summary = generate_ai_summary(biomarkers)

    return {"biomarker_analysis": analysis, "ai_summary": ai_summary}