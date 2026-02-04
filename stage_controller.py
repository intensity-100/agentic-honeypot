def update_stage(session: dict):
    turns = session["turns"]
    intel = session["intelligence"]

    # If we already reached closing, stay there
    if session["stage"] == "closing":
        return

    # Fast-forward to closing if intel collected
    if intel["upi"] or intel["links"] or intel["bank_accounts"]:
        session["stage"] = "closing"
        return

    # Normal progression by turns
    if turns >= 8 and session["stage"] == "baiting":
        session["stage"] = "trust"
        return

    if turns >= 12 and session["stage"] == "trust":
        session["stage"] = "extraction"
        return
