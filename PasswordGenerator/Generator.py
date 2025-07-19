import random
import string
import re

def generate_strong_password(length=16):
    # Mix of upper/lowercase, digits, symbols
    chars = string.ascii_letters + string.digits + string.punctuation
    rng = random.SystemRandom()

    while True:
        pwd = ''.join(rng.choice(chars) for _ in range(length))
        strength, _ = check_password_strength(pwd)
        if strength == "strong":
            return pwd
        
def check_password_strength(password):
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