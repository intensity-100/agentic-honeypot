import random

ELDERLY_REPLIES = {
    "baiting": [
        "I don’t understand all this, beta. What is happening?",
        "Why will my account be blocked? I am very scared.",
        "This phone confuses me. Can you tell slowly?"
    ],
    "trust": [
        "You are from the bank only, no?",
        "My son usually helps me, but he is not here.",
        "I am old, please explain again."
    ],
    "extraction": [
        "Which app should I open? There are many.",
        "Can you write the number slowly?",
        "Is this Google Pay or PhonePe?"
    ],
    "closing": [
        "My battery is going low, wait.",
        "I will go to bank branch nearby.",
        "Let me call my son once."
    ]
}

def get_persona_reply(stage: str) -> str:
    responses = ELDERLY_REPLIES.get(stage, ELDERLY_REPLIES["baiting"])
    return random.choice(responses)
