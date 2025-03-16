import random
import string
from app.libs.checkSyntax import check_is_email
import re


def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))


def check_is_email(email: str) -> bool:
    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return pattern.fullmatch(email) is not None
