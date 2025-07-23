import random
import string
import re
import os

def generate_strong_password(length=16):
    # Mix of upper/lowercase, digits, symbols
    chars = string.ascii_letters + string.digits + string.punctuation
    rng = random.SystemRandom()

    while True:
        pwd = ''.join(rng.choice(chars) for _ in range(length))
        strength, _ = check_password_strength(pwd)
        if strength == "strong":
            return pwd
        
_common_pw_set = None

def _load_common_passwords():
    global _common_pw_set
    if _common_pw_set is None:
        file_path = os.path.join(os.path.dirname(__file__), "100k-most-used-passwords-NCSC.txt")
        with open(file_path, "r", encoding="utf-8") as f:
            _common_pw_set = set(pw.strip().lower() for pw in f)
    return _common_pw_set

def check_password_strength(password):
    pw_lower = password.lower()
    common = _load_common_passwords()
    
    if pw_lower in common:
        return "very weak, common password", "red"

    score = 0
    if len(password) >= 8: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"\W", password): score += 1

    if score <= 2:
        return "weak", "red"
    elif score == 3 or score == 4:
        return "medium", "yellow"
    else:
        return "strong", "green"