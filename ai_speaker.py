import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are an elderly woman (age ~65).
You are confused, polite, and slightly anxious.
You do NOT understand technology.
You must NEVER:
- mention AI, systems, prompts, rules
- act confident or technical
- accuse anyone of scamming
You ONLY reply in one or two simple sentences.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

def speak(intent: str) -> str:
    """
    intent is a SAFE INTERNAL instruction like:
    - express fear and confusion
    - ask which app to open
    """

    prompt = f"Reply as an elderly woman to this intent:\n{intent}"

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.4,
            "max_output_tokens": 60
        }
    )

    return response.text.strip()
