import re

def check_is_email(email: str) -> bool:
    return True if re.match(r"[^@]+@[^@]+\.[^@]+", email) else False
