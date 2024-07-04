

import re
import random
import string
import tkinter as tk
from tkinter import messagebox

def evaluate_password(password):
    length_criteria = len(password) >= 8
    lower_case = re.search(r'[a-z]', password)
    upper_case = re.search(r'[A-Z]', password)
    digit = re.search(r'\d', password)
    special_char = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)

    strength_score = sum([length_criteria, bool(lower_case), bool(upper_case), bool(digit), bool(special_char)])
    
    if strength_score <= 2:
        return "Weak", "red"
    elif strength_score == 3:
        return "Medium", "orange"
    elif strength_score >= 4:
        return "Strong", "green"

def recommend_practices():
    recommendations = [
        "Use at least 8 characters.",
        "Include both uppercase and lowercase letters.",
        "Include at least one number.",
        "Include at least one special character (!@#$%^&*(), etc.).",
        "Avoid common passwords and patterns."
    ]
    return recommendations

def generate_strong_password():
    length = 12
    all_chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_chars) for _ in range(length))
    return password

def suggest_passwords():
    passwords = [generate_strong_password() for _ in range(5)]
    messagebox.showinfo("Password Suggestions", "\n".join(passwords))

def evaluate_password_event():
    password = entry.get()
    strength, color = evaluate_password(password)
    result_label.config(text=f"Strength: {strength}", fg=color)
    
    if strength == "Weak":
        practices = recommend_practices()
        suggested_password = generate_strong_password()
        messagebox.showwarning(
            "Weak Password",
            f"{' '.join(practices)}\n\nSuggested Password: {suggested_password}"
        )

app = tk.Tk()
app.title("Password Analyzer")

frame = tk.Frame(app, padx=10, pady=10)
frame.pack(padx=10, pady=10)

entry_label = tk.Label(frame, text="Enter Password:")
entry_label.grid(row=0, column=0, pady=5)

entry = tk.Entry(frame, show="*", width=30)
entry.grid(row=0, column=1, pady=5)

evaluate_button = tk.Button(frame, text="Evaluate", command=evaluate_password_event)
evaluate_button.grid(row=1, columnspan=2, pady=10)

suggest_button = tk.Button(frame, text="Suggest Passwords", command=suggest_passwords)
suggest_button.grid(row=2, columnspan=2, pady=10)

result_label = tk.Label(frame, text="Strength: ", font=('Helvetica', 12, 'bold'))
result_label.grid(row=3, columnspan=2, pady=5)

app.mainloop()
