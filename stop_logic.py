def should_stop(session: dict) -> bool:
    if session["stage"] == "closing":
        return True

    if session["turns"] >= 18:
        return True

    return False
