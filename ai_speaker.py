import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash"
)

def speak(intent, last_scammer_message, stage):
    prompt = f"""
You are a real retired Indian woman in your mid-60s.
You speak naturally and think out loud.
You are cautious, not fearful.
You dislike rushed instructions.

You just received this message:
"{last_scammer_message}"

You are thinking:
{intent}

Respond naturally in 1–2 sentences.
"""


    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 80
        }
    )

    return response.text.strip()
