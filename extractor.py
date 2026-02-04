import re

UPI_REGEX = re.compile(r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}")
URL_REGEX = re.compile(r"https?://[^\s]+")
PHONE_REGEX = re.compile(r"\+91\d{10}")
BANK_REGEX = re.compile(r"\b\d{9,18}\b")

def extract_intelligence(text: str) -> dict:
    return {
        "upi": list(set(UPI_REGEX.findall(text))),
        "links": list(set(URL_REGEX.findall(text))),
        "phones": list(set(PHONE_REGEX.findall(text))),
        "bank_accounts": list(set(BANK_REGEX.findall(text)))
    }
