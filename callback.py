import requests

GUVI_ENDPOINT ="https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_callback(session: dict):
    payload = {
        "sessionId": session["session_id"],
        "scamDetected": True,
        "totalMessagesExchanged": session["turns"],
        "extractedIntelligence": {
            "bankAccounts": session["intelligence"]["bank_accounts"],
            "upiIds": session["intelligence"]["upi"],
            "phishingLinks": session["intelligence"]["links"],
            "phoneNumbers": session["intelligence"]["phones"],
            "suspiciousKeywords": []  # optional
        },
        "agentNotes": "Urgency tactics, authority impersonation, payment redirection"
    }

    response = requests.post(
        GUVI_ENDPOINT,
        json=payload,
        timeout=5
    )

    response.raise_for_status()
