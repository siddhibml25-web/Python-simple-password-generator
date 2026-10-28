import string
import secrets

import streamlit as st

SYMBOLS = "!@#$%^&*()-_=+[]{}<>?"

st.set_page_config(page_title="Password Generator", page_icon="🔐")
st.title("🔐 PASSWORD GENERATOR")


def get_password(length, use_upper, use_lower, use_digits, use_symbols):
    groups = []
    if use_upper:
        groups.append(string.ascii_uppercase)
    if use_lower:
        groups.append(string.ascii_lowercase)
    if use_digits:
        groups.append(string.digits)
    if use_symbols:
        groups.append(SYMBOLS)

    if not groups:
        raise ValueError("Select at least one character type.")
    if length < len(groups):
        raise ValueError("Length is too small for selected types.")

    password = [secrets.choice(group) for group in groups]
    all_chars = "".join(groups)
    password.extend(secrets.choice(all_chars) for _ in range(length - len(password)))
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def check_strength(password):
    score = sum([
        len(password) >= 8,
        len(password) >= 12,
        any(c.isupper() for c in password),
        any(c.islower() for c in password),
        any(c.isdigit() for c in password),
        any(c in SYMBOLS for c in password),
    ])
    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    return "Strong"


length = st.number_input("Password Length", min_value=4, max_value=128, value=12, step=1)

st.subheader("Choose Character Types")
use_upper = st.checkbox("Uppercase Letters (A-Z)", value=True)
use_lower = st.checkbox("Lowercase Letters (a-z)", value=True)
use_digits = st.checkbox("Numbers (0-9)", value=True)
use_symbols = st.checkbox("Special Symbols (!@#$...)", value=True)

if st.button("Generate Password", type="primary"):
    try:
        st.session_state["password"] = get_password(
            int(length), use_upper, use_lower, use_digits, use_symbols
        )
    except ValueError as e:
        st.error(str(e))

if "password" in st.session_state:
    pwd = st.session_state["password"]
    st.subheader("Generated Password")
    show = st.checkbox("Show Password", value=False)
    if show:
        st.code(pwd, language=None)
    else:
        st.code("*" * len(pwd), language=None)
        st.caption("Tick 'Show Password' to see and copy it.")

    strength = check_strength(pwd)
    color = {"Weak": "red", "Medium": "orange", "Strong": "green"}[strength]
    st.markdown(f"**Password Strength:** :{color}[{strength}]")

st.divider()
st.subheader("Generate Multiple Passwords")
count = st.number_input("Number of Passwords", min_value=1, max_value=50, value=5, step=1)

if st.button("Generate Multiple Passwords"):
    try:
        passwords = [
            get_password(int(length), use_upper, use_lower, use_digits, use_symbols)
            for _ in range(int(count))
        ]
        st.session_state["many"] = "\n".join(passwords)
    except ValueError as e:
        st.error(str(e))

if "many" in st.session_state:
    st.code(st.session_state["many"], language=None)