def validate_email(email):
    if '@' in email and '.' in email:
        return True
    return False