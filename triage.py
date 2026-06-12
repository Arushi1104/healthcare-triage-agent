import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_triage(patient_message: str) -> dict:
    
    prompt = f"""
You are a medical triage assistant for rural healthcare. A patient has sent the following message:

Patient: {patient_message}

Your job is to assess urgency. Respond ONLY in this exact JSON format, nothing else:

{{
  "triage_level": "monitor at home" or "see a doctor soon" or "seek urgent care",
  "patient_summary": "2-3 sentence plain language explanation for the patient",
  "clinician_summary": "structured clinical summary with symptoms, duration, urgency",
  "follow_up_question": "ask ONE missing detail if critical info is absent, otherwise leave as empty string"
}}

Rules:
- If you don't know duration, severity, or age — ask in follow_up_question
- If follow_up_question is not empty, triage_level should be "pending"
- Never diagnose, only triage
- Keep patient_summary simple, no medical jargon
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()
    
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "triage_level": "pending",
            "patient_summary": "Sorry, I could not process your message. Please describe your symptoms clearly.",
            "clinician_summary": "Parse error on input.",
            "follow_up_question": "Could you describe your symptoms in more detail?"
        }
    
    return result