import re
import getpass

COMMON_PASSWORDS = {
    "password", "password123", "123456", "123456789",
    "qwerty", "admin", "letmein", "welcome", "iloveyou"
}

def check_password(password: str):
    """Return a strength score, rating, and improvement suggestions."""
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if len(password) >= 12:
        score += 1
    else:
        suggestions.append("Aim for 12 or more characters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add at least one lowercase letter.")

    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Add at least one number.")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        suggestions.append("Add at least one special character (such as !, @, #, or $).")

    if password.lower() in COMMON_PASSWORDS:
        score = 0
        suggestions.append("Avoid common passwords.")

    if re.search(r"(.)\1{2,}", password):
        score = max(0, score - 1)
        suggestions.append("Avoid repeating the same character three or more times.")

    if re.search(r"(123|234|345|456|567|678|789|abc|bcd|cde|qwe)", password.lower()):
        score = max(0, score - 1)
        suggestions.append("Avoid predictable sequences.")

    if score <= 2:
        rating = "Weak"
    elif score <= 4:
        rating = "Moderate"
    else:
        rating = "Strong"

    return score, rating, suggestions


def main():
    print("=" * 42)
    print("       PASSWORD STRENGTH CHECKER")
    print("=" * 42)
    print("Your password is checked locally; it is not sent anywhere.")
    password = getpass.getpass("\nEnter a password to check: ")

    score, rating, suggestions = check_password(password)

    print(f"\nStrength: {rating} ({score}/6)")
    if suggestions:
        print("\nSuggestions:")
        for item in suggestions:
            print(f"- {item}")
    else:
        print("Great! Your password meets all the basic checks.")

    print("\nTip: Use a unique password for every account.")
    print("A password manager can help you create and store strong passwords.")


if __name__ == "__main__":
    main()
