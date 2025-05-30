import re

def is_strong_password(password):
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"\d", password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return False
    return True