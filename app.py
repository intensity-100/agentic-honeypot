from fastapi import FastAPI, Header, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field

from config import API_KEY
from state import get_session
from detector import detect_scam
from persona import get_persona_reply
from delay import human_delay
from ai_speaker import speak
from extractor import extract_intelligence
from stage_controller import update_stage
from stop_logic import should_stop
from callback import send_final_callback

app = FastAPI()


# ---------- REQUEST MODELS ----------
class Message(BaseModel):
    sender: str = Field(..., example="scammer")
    text: str = Field(..., example="Your bank account will be blocked")
    timestamp: int = Field(..., example=1770005528731)


class ConversationItem(BaseModel):
    sender: str
    text: str
    timestamp: int


class Metadata(BaseModel):
    channel: Optional[str] = "SMS"
    language: Optional[str] = "English"
    locale: Optional[str] = "IN"


class IncomingMessage(BaseModel):
    sessionId: str = Field(..., min_length=1)
    message: Message
    conversationHistory: List[ConversationItem] = []
    metadata: Optional[Metadata] = None


# ---------- ROOT FALLBACK (FOR TESTERS) ----------
@app.post("/")
def root_fallback():
    return {
        "status": "success",
        "message": "Honeypot API is live"
    }


# ---------- AGENT INTENT CONTROLLER ----------
import random

def decide_intent(stage: str) -> str:
    if stage == "baiting":
        return random.choice([
            "express fear and ask what is happening",
            "say you are scared and don’t understand this message",
            "say you are worried and ask why this is happening"
        ])

    if stage == "trust":
        return random.choice([
            "ask them to explain again slowly",
            "say you are old and need simple explanation"
        ])

    if stage == "extraction":
        return random.choice([
            "ask which app to open",
            "ask where exactly to send money",
            "ask them to write the number slowly"
        ])

    if stage == "closing":
        return "say you will go to the bank or ask your son for help"

    return "express confusion"


# ---------- MAIN API ----------
@app.post("/honeypot/message")
def honeypot_entry(
    payload: IncomingMessage,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    session = get_session(payload.sessionId)
    incoming_text = payload.message.text

    # Store message safely
    session["messages"].append(payload.message.dict())
    session["turns"] += 1

    # Scam detection (one-way lock)
    if not session["scam_confirmed"]:
        if detect_scam(incoming_text):
            session["scam_confirmed"] = True
            session["agent_active"] = True

    # Intelligence extraction (only from scammer)
    if session["scam_confirmed"] and payload.message.sender == "scammer":
        extracted = extract_intelligence(incoming_text)

        for key in extracted:
            for value in extracted[key]:
                if value not in session["intelligence"][key]:
                    session["intelligence"][key].append(value)

    # Update agent stage
    if session["scam_confirmed"]:
        update_stage(session)

    # Reply logic
    if session["scam_confirmed"]:
        if should_stop(session):
            reply = get_persona_reply("closing")
        else:
            human_delay(session["stage"])
            intent = decide_intent(session["stage"])

            try:
                reply = speak(
                    intent=intent,
                    last_scammer_message=incoming_text,
                    stage=session["stage"]
                )
                if not reply or len(reply.strip())< 8:
                    raise ValueError("Gemini returned weak response")
            except Exception as e:
                print("❌", e)
                reply = get_persona_reply(session["stage"])
    else:
        reply = "Sorry, I don’t understand."

    # Final callback (only once)
    if (
        session["scam_confirmed"]
        and should_stop(session)
        and not session["final_callback_sent"]
    ):
        try:
            send_final_callback(session)
            session["final_callback_sent"] = True
        except Exception as e:
            print("Callback failed:", e)

    return {
        "status": "success",
        "reply": reply
    }
