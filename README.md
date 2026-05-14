# Password Analyzer

A simple Python tool to check how strong your password is. It looks at length, uppercase/lowercase letters, numbers, and special characters.

## How it works
The script checks for 5 main things:
1. Is it at least 8 characters long?
2. Does it have an uppercase letter?
3. Does it have a lowercase letter?
4. Does it have a number?
5. Does it have a special character?

Based on these, it gives you a score from 0 to 5 and tells you if your password is Weak, Medium, or Strong.

## How to Run
1. Make sure you have Python installed.
2. Run the script:
   ```bash
   python password_analyzer.py
   ```

## Example
```text
Enter a password to analyze: MyPass123!

Analysis for: *********
STRENGTH: 🟢 STRONG
Score: 5/5
Great! This is a strong password.
```
