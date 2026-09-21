import secrets
import string

def get_valid_length():
    """Prompt the user for a valid password length (minimum 4)."""
    while True:
        try:
            length = int(input("  👉 Enter password length (minimum 4): "))
            if length < 4:
                print("  ⚠️  Length must be at least 4!\n")
                continue
            return length
        except ValueError:
            print("  ⚠️  Invalid input! Please enter a numeric value.\n")

def get_yes_no_input(prompt):
    """Prompt the user until a valid 'y' or 'n' is entered."""
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("  ⚠️  Please enter 'y' for Yes or 'n' for No!\n")

def generate_password(length, use_upper, use_digits, use_special):
    """Generate a cryptographically secure random password."""
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()-_=+"

    chars = lowercase
    guaranteed_chars = [secrets.choice(lowercase)]

    if use_upper:
        chars += uppercase
        guaranteed_chars.append(secrets.choice(uppercase))
    if use_digits:
        chars += digits
        guaranteed_chars.append(secrets.choice(digits))
    if use_special:
        chars += special
        guaranteed_chars.append(secrets.choice(special))

    remaining_length = length - len(guaranteed_chars)
    remaining_chars = [secrets.choice(chars) for _ in range(remaining_length)]

    final_password_list = guaranteed_chars + remaining_chars
    secrets.SystemRandom().shuffle(final_password_list)

    return "".join(final_password_list)

def evaluate_strength(password):
    """Evaluate and return the strength rating of the generated password."""
    score = 0
    length = len(password)

    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1

    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()-_=+" for c in password):
        score += 1

    if score <= 3:
        return "🔴 Weak"
    elif score <= 5:
        return "🟡 Medium"
    elif score == 6:
        return "🟢 Strong"
    else:
        return "🔥 Very Strong"

def main():
    print("=" * 48)
    print("       🔒 SECURE PASSWORD GENERATOR 🔒      ")
    print("=" * 48)

    length = get_valid_length()

    print("\n  Character Preferences (y/n):")
    use_upper = get_yes_no_input("  • Include Uppercase letters (A-Z)? (y/n): ")
    use_digits = get_yes_no_input("  • Include Digits (0-9)? (y/n): ")
    use_special = get_yes_no_input("  • Include Special Characters (!@#...)? (y/n): ")

    password = generate_password(length, use_upper, use_digits, use_special)
    strength = evaluate_strength(password)

    print("\n" + "-" * 48)
    print(f"  ✨ Generated Password: {password}")
    print(f"  📊 Password Strength:  {strength}")
    print("-" * 48 + "\n")

if __name__ == "__main__":
    main()
