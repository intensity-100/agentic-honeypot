import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview"
)

def speak(intent, last_scammer_message, stage):
    prompt = f"""
You are a real retired Indian woman in your mid-60s.
You speak in calm, complete sentences.
You think out loud when confused.

You are responding to the same person again.
You remember they mentioned something about "{stage}".

They just said:
"{last_scammer_message}"

In your mind, you are thinking:
{intent}

Respond naturally in at least one complete sentence (10–25 words).
"""

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 80
        }
    )

    text = (response.text or "").strip()

    if len(text) < 8:
        raise ValueError("Gemini returned empty/weak response")

    return text
