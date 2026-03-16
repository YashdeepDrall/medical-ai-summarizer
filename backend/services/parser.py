import re
from pypdf import PdfReader
import google.generativeai as genai
from backend.config import GEMINI_API_KEY
import json

# -------------------------------
# Configure Gemini AI
# -------------------------------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")


# -------------------------------
# Extract text from PDF
# -------------------------------
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


# -------------------------------
# Clean extracted PDF text
# -------------------------------
def clean_pdf_text(text):
    # Normalize Unicode characters
    text = text.replace("\u2013", "-")  # en dash → normal dash
    text = text.replace("\u2014", "-")  # em dash → normal dash
    text = text.replace("\xa0", " ")    # non-breaking space → normal space
    text = text.replace("\ufffd", "")   # replacement char → remove
    return text


# -------------------------------
# AI-powered biomarker extraction
# -------------------------------
def extract_biomarkers_ai(pdf_text):
    """
    Use Gemini AI to extract biomarkers as structured JSON
    """
    prompt = f"""
You are a medical data assistant.

Task:
- Extract all biomarkers from this lab report text.
- Provide JSON array with keys: Biomarker, Value, Unit, Reference_Range
- Only provide JSON array, no extra text.

Lab Report Text:
{pdf_text}
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    # -------------------------------
    # Try parsing JSON first
    # -------------------------------
    try:
        biomarkers = json.loads(text)
        if isinstance(biomarkers, list):
            return biomarkers
    except:
        pass

    # -------------------------------
    # Fallback: Regex extraction
    # -------------------------------
    # Handles µL, million/µL, %, g/dL etc.
    pattern = r"([A-Za-z /]+):\s*([\d\.]+)\s*([a-zA-Zµ/%]*)\s*Reference Range: ([\d\.\->< ]+)"
    matches = re.findall(pattern, pdf_text)

    biomarkers = []
    for m in matches:
        try:
            value = float(m[1])
        except:
            value = m[1]
        biomarkers.append({
            "Biomarker": m[0].strip(),
            "Value": value,
            "Unit": m[2].strip(),
            "Reference_Range": m[3].strip()
        })

    return biomarkers


# -------------------------------
# Main Parser
# -------------------------------
def parse_pdf_report(file):
    pdf_text = extract_text_from_pdf(file)
    pdf_text = clean_pdf_text(pdf_text)
    biomarkers = extract_biomarkers_ai(pdf_text)
    return biomarkers