from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

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
from typing import List, Optional

app = FastAPI()

class IncomingMessage(BaseModel):
    sessionId: str
    message: dict
    conversationHistory: Optional[List[dict]] = []
    metadata: Optional[dict] = {}


# ---------- AGENT INTENT CONTROLLER ----------
def decide_intent(stage: str) -> str:
    if stage == "baiting":
        return "express fear and ask what is happening"
    if stage == "trust":
        return "ask them to explain again slowly"
    if stage == "extraction":
        return "ask which app or number to use"
    if stage == "closing":
        return "say you will go to bank or call son"
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
    incoming_text = payload.message.get("text", "")

    # Store message
    session["messages"].append(payload.message)
    session["turns"] += 1

    # Scam detection (one-way lock)
    if not session["scam_confirmed"]:
        if detect_scam(incoming_text):
            session["scam_confirmed"] = True
            session["agent_active"] = True

    # Intelligence extraction (only from scammer)
    if session["scam_confirmed"] and payload.message.get("sender") == "scammer":
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

        # Stop condition
        if should_stop(session):
            reply = get_persona_reply("closing")
        else:
            human_delay(session["stage"])
            intent = decide_intent(session["stage"])

            try:
                reply = speak(intent)
            except Exception:
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
        "reply": reply,
        "debug": {
            "turns": session["turns"],
            "stage": session["stage"],
            "intelligence": session["intelligence"]
        }
    }
