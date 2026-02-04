from typing import Dict, Any

# In-memory session store (later can be Redis)
SESSIONS: Dict[str, Dict[str, Any]] = {}

def get_session(session_id: str) -> Dict[str, Any]:
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {
            "session_id": session_id,
            "messages": [],
            "turns": 0,
            "scam_confirmed": False,
            "agent_active": False,
            "stage": "baiting",
            "final_callback_sent": False,
            "intelligence": {
                "upi": [],
                "links": [],
                "phones": [],
                "bank_accounts": []
            }
        }
    return SESSIONS[session_id]
