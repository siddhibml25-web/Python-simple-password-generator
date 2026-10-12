
import tkinter as tk
from tkinter import messagebox
import string
import secrets

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator - Phase 3")
        self.root.geometry("560x620")
        self.root.configure(bg="#edf2f7")

        self.upper = tk.BooleanVar(value=True)
        self.lower = tk.BooleanVar(value=True)
        self.digits = tk.BooleanVar(value=True)
        self.symbols = tk.BooleanVar(value=True        self.show_password = tk.BooleanVar(value=False)

        tk.Label(root, text="PASSWORD GENERATOR",
                 font=("Arial", 19, "bold"),
                 bg="#edf2f7", fg="#183153").pack(pady=15)

        tk.Label(root, text="Password Length:",
                 bg="#edf2f7", font=("Arial", 11)).pack()

        self.length = tk.Entry(root, justify="center", font=("Arial", 12))
        self.length.insert(0, "12")
        self.length.pack(pady=5)

        tk.Label(root, text="Choose Character Types",
                 bg="#edf2f7", font=("Arial", 12, "bold")).pack(pady=8)

        for label, variable in [
            ("Uppercase Letters (A-Z)", self.upper),
            ("Lowercase Letters (a-z)", self.lower),
            ("Numbers (0-9)", self.digits),
            ("Special Symbols (!@#$...)", self.symbols)
        ]:
            tk.Checkbutton(root, text=label, variable=variable,
                           bg="#edf2f7").pack(anchor="w", padx=150)

        tk.Label(root, text="Generated Password:",
                 bg="#edf2f7", font=("Arial", 11)).pack(pady=(12, 3))

        self.password = tk.Entry(root, width=38, justify="center",
                                 font=("Arial", 12), show="*")
        self.password.pack(pady=5)

        tk.Checkbutton(root, text="Show Password",
                       variable=self.show_password,
                       command=self.toggle_password,
                       bg="#edf2f7").pack()

        tk.Button(root, text="Generate Password",
                  command=self.generate_one,
                  bg="#2563eb", fg="white", width=22).pack(pady=6)

        tk.Button(root, text="Copy Password",
                  command=self.copy_password,
                  width=22).pack(pady=4)

        tk.Label(root, text="Password Strength:",
                 bg="#edf2f7", font=("Arial", 11)).pack(pady=(8, 2))

        self.strength = tk.Label(root, text="Not generated",
                                 bg="#edf2f7", font=("Arial", 12, "bold"))
        self.strength.pack()

        tk.Label(root, text="Number of Passwords to Generate:",
                 bg="#edf2f7").pack(pady=(12, 3))

        self.count = tk.Entry(root, justify="center")
        self.count.insert(0, "5")
        self.count.pack()

        tk.Button(root, text="Generate Multiple Passwords",
                  command=self.generate_multiple,
                  bg="#0f766e", fg="white", width=25).pack(pady=8)

        self.results = tk.Text(root, height=6, width=55)
        self.results.pack(padx=10, pady=5)

        tk.Button(root, text="Copy Selected Password",
                  command=self.copy_selected).pack(pady=5)

    def get_password(self):
        try:
            length = int(self.length.get())
        except ValueError:
            raise ValueError("Enter a valid password length.")

        if length < 4 or length > 128:
            raise ValueError("Length must be between 4 and 128.")

        groups = []

        if self.upper.get():
            groups.append(string.ascii_uppercase)
        if self.lower.get():
            groups.append(string.ascii_lowercase)
        if self.digits.get():
            groups.append(string.digits)
        if self.symbols.get():
            groups.append("!@#$%^&*()-_=+[]{}<>?")

        if not groups:
            raise ValueError("Select at least one character type.")

        if length < len(groups):
            raise ValueError("Length is too small for selected types.")

        password = [secrets.choice(group) for group in groups]
        all_chars = "".join(groups)

        password.extend(
            secrets.choice(all_chars)
            for _ in range(length - len(password))
        )

        secrets.SystemRandom().shuffle(password)
        return "".join(password)

    def check_strength(self, password):
        score = sum([
            len(password) >= 8,
            len(password) >= 12,
            any(c.isupper() for c in password),
            any(c.islower() for c in password),
            any(c.isdigit() for c in password),
            any(c in "!@#$%^&*()-_=+[]{}<>?" for c in password)
        ])

        if score <= 2:
            return "Weak"
        elif score <= 4:
            return "Medium"
        return "Strong"

    def generate_one(self):
        try:
            password = self.get_password()
            self.password.delete(0, tk.END)
            self.password.insert(0, password)
            self.strength.config(text=self.check_strength(password))
            self.results.delete("1.0", tk.END)
        except ValueError as error:
            messagebox.showerror("Input Error", str(error))

    def generate_multiple(self):
        try:
            count = int(self.count.get())
            if count < 1 or count > 50:
                raise ValueError("Enter a number between 1 and 50.")

            passwords = [self.get_password() for _ in range(count)]
            self.results.delete("1.0", tk.END)
            self.results.insert(tk.END, "\n".join(passwords))
        except ValueError as error:
            messagebox.showerror("Input Error", str(error))

    def toggle_password(self):
        self.password.config(show="" if self.show_password.get() else "*")

    def copy_password(self):
        password = self.password.get()
        if not password:
            messagebox.showwarning("Warning", "Generate a password first.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied.")

    def copy_selected(self):
        try:
            selected = self.results.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected.strip())
            messagebox.showinfo("Copied", "Selected text copied.")
        except tk.TclError:
            messagebox.showwarning("Warning", "Select a password first.")

root = tk.Tk()
app = PasswordGenerator(root)
root.mainloop()
