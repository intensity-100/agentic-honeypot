SCAM_KEYWORDS = [
    "account blocked",
    "account suspended",
    "verify immediately",
    "urgent",
    "share otp",
    "upi",
    "click link",
    "kyc",
    "bank account",
    "payment failure"
]

def detect_scam(text: str) -> bool:
    if not text:
        return False

    lowered = text.lower()

    for keyword in SCAM_KEYWORDS:
        if keyword in lowered:
            return True

    return False
