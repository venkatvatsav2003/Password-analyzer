import tkinter as tk
from tkinter import messagebox, ttk
import re
import random
import string
import math
import hashlib
import requests

class PasswordAnalyzer:
    @staticmethod
    def calculate_entropy(password):
        if not password:
            return 0
        
        pool_size = 0
        if re.search(r'[a-z]', password):
            pool_size += 26
        if re.search(r'[A-Z]', password):
            pool_size += 26
        if re.search(r'\d', password):
            pool_size += 10
        if re.search(r'[^a-zA-Z\d]', password):
            pool_size += 32 # Approximation for special characters

        if pool_size == 0:
            return 0

        entropy = len(password) * math.log2(pool_size)
        return round(entropy, 2)

    @staticmethod
    def check_pwned(password):
        try:
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix, suffix = sha1_hash[:5], sha1_hash[5:]
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            hashes = (line.split(':') for line in response.text.splitlines())
            for h, count in hashes:
                if h == suffix:
                    return int(count)
            return 0
        except requests.exceptions.RequestException:
            return -1 # Indicate network error or API failure

    @classmethod
    def evaluate(cls, password):
        if not password:
             return {"score": 0, "strength": "Very Weak", "color": "red", "feedback": ["Password cannot be empty."], "entropy": 0, "pwned": 0}

        entropy = cls.calculate_entropy(password)
        pwned_count = cls.check_pwned(password)
        
        score = 0
        feedback = []

        if len(password) < 8:
            feedback.append("Password should be at least 8 characters long.")
        elif len(password) >= 12:
            score += 2
        else:
            score += 1
            feedback.append("Consider using 12 or more characters.")

        if not re.search(r'[A-Z]', password):
            feedback.append("Add uppercase letters.")
        else:
            score += 1
            
        if not re.search(r'[a-z]', password):
            feedback.append("Add lowercase letters.")
        else:
            score += 1

        if not re.search(r'\d', password):
            feedback.append("Add numbers.")
        else:
            score += 1

        if not re.search(r'[^a-zA-Z\d]', password):
            feedback.append("Add special characters (e.g., !@#$%).")
        else:
            score += 1

        if pwned_count > 0:
            score = 0 # Compromised passwords are automatically very weak
            feedback.insert(0, f"DANGER: Password has been compromised {pwned_count} times!")
        elif pwned_count == -1:
             feedback.append("Warning: Could not check compromised password database.")

        # Entropy based adjustment
        if entropy < 35:
            score = min(score, 2) # Cap score if entropy is too low
        elif entropy > 60:
            score = min(score + 1, 6)

        strength_mapping = {
            0: ("Very Weak", "red"),
            1: ("Weak", "red"),
            2: ("Weak", "orange red"),
            3: ("Medium", "orange"),
            4: ("Strong", "light green"),
            5: ("Very Strong", "green"),
            6: ("Excellent", "dark green")
        }

        strength, color = strength_mapping.get(min(score, 6), ("Unknown", "grey"))
        
        if not feedback and score >= 4:
             feedback.append("Great password!")

        return {
            "score": score,
            "strength": strength,
            "color": color,
            "feedback": feedback,
            "entropy": entropy,
            "pwned": pwned_count
        }

    @staticmethod
    def generate_strong_password(length=16):
        if length < 8:
            length = 8
        all_chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
        password = ''.join(random.choice(all_chars) for _ in range(length))
        # Ensure at least one of each type
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password) or not re.search(r'[^a-zA-Z\d]', password):
             return PasswordAnalyzer.generate_strong_password(length)
        return password

class PasswordAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Analyzer")
        self.root.geometry("450x450")
        self.root.configure(padx=20, pady=20)

        self.create_widgets()

    def create_widgets(self):
        # Entry
        tk.Label(self.root, text="Enter Password:", font=('Helvetica', 10, 'bold')).pack(anchor="w")
        
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(fill="x", pady=(5, 15))
        
        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self.on_password_change)
        
        self.entry = ttk.Entry(entry_frame, textvariable=self.password_var, show="*", font=('Helvetica', 12))
        self.entry.pack(side="left", fill="x", expand=True)

        self.toggle_btn = ttk.Button(entry_frame, text="Show", command=self.toggle_visibility, width=6)
        self.toggle_btn.pack(side="right", padx=(5, 0))

        # Strength Bar
        self.strength_label = tk.Label(self.root, text="Strength: None", font=('Helvetica', 12, 'bold'))
        self.strength_label.pack(anchor="w")
        
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(fill="x", pady=(5, 15))

        # Details Frame
        details_frame = tk.LabelFrame(self.root, text="Analysis Details", padx=10, pady=10)
        details_frame.pack(fill="both", expand=True, pady=(0, 15))

        self.entropy_label = tk.Label(details_frame, text="Entropy: 0 bits")
        self.entropy_label.pack(anchor="w")

        self.pwned_label = tk.Label(details_frame, text="Pwned Status: Not Checked")
        self.pwned_label.pack(anchor="w")

        tk.Label(details_frame, text="Feedback:").pack(anchor="w", pady=(5, 0))
        self.feedback_text = tk.Text(details_frame, height=5, width=40, wrap="word", state="disabled", bg=self.root.cget('bg'), relief="flat")
        self.feedback_text.pack(fill="both", expand=True)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Generate Strong Password", command=self.generate_password).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(btn_frame, text="Clear", command=self.clear_fields).pack(side="right", expand=True, fill="x", padx=(5, 0))

    def toggle_visibility(self):
        if self.entry.cget('show') == '':
            self.entry.config(show='*')
            self.toggle_btn.config(text='Show')
        else:
            self.entry.config(show='')
            self.toggle_btn.config(text='Hide')

    def on_password_change(self, *args):
        password = self.password_var.get()
        if not password:
            self.reset_ui()
            return

        # Simple debounce or direct evaluation
        result = PasswordAnalyzer.evaluate(password)
        self.update_ui(result)

    def update_ui(self, result):
        self.strength_label.config(text=f"Strength: {result['strength']}", fg=result['color'])
        
        # Update progress bar (Score 0-6 maps to 0-100)
        self.progress['value'] = (result['score'] / 6) * 100

        self.entropy_label.config(text=f"Entropy: {result['entropy']} bits")
        
        if result['pwned'] > 0:
             self.pwned_label.config(text=f"Pwned Status: COMPROMISED ({result['pwned']} times)", fg="red")
        elif result['pwned'] == -1:
             self.pwned_label.config(text="Pwned Status: Check Failed", fg="orange")
        else:
             self.pwned_label.config(text="Pwned Status: Safe (0 times)", fg="green")

        self.feedback_text.config(state="normal")
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.insert(tk.END, "\n".join(f"- {f}" for f in result['feedback']))
        self.feedback_text.config(state="disabled")

    def reset_ui(self):
        self.strength_label.config(text="Strength: None", fg="black")
        self.progress['value'] = 0
        self.entropy_label.config(text="Entropy: 0 bits")
        self.pwned_label.config(text="Pwned Status: Not Checked", fg="black")
        self.feedback_text.config(state="normal")
        self.feedback_text.delete(1.0, tk.END)
        self.feedback_text.config(state="disabled")

    def generate_password(self):
        new_password = PasswordAnalyzer.generate_strong_password()
        self.password_var.set(new_password)
        if self.entry.cget('show') == '*':
            self.toggle_visibility()

    def clear_fields(self):
        self.password_var.set("")
        if self.entry.cget('show') == '':
            self.toggle_visibility()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordAnalyzerApp(root)
    root.mainloop()
