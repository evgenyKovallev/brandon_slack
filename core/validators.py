def validate_email_post(data: dict) -> bool:
    if data.get('emails') and isinstance(data.get('emails'), list):
        return True
    else:
        return False
