import re

def analyze_password(password):
    score = 0
    feedback = []

    # 1. Check length
    if len(password) < 8:
        feedback.append("Too short (minimum 8 characters)")
    else:
        score += 1

    # 2. Check for uppercase letters
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters (A-Z)")

    # 3. Check for lowercase letters
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters (a-z)")

    # 4. Check for numbers
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers (0-9)")

    # 5. Check for special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add special characters (!@#$%^&*)")

    return score, feedback

def main():
    print("--- Simple Password Analyzer ---")
    
    while True:
        password = input("\nEnter a password to analyze (or 'exit' to quit): ")
        
        if password.lower() == 'exit':
            break
            
        if not password:
            print("Password cannot be empty!")
            continue

        score, feedback = analyze_password(password)
        
        print(f"\nAnalysis for: {'*' * len(password)}")
        
        if score <= 2:
            print("STRENGTH: 🔴 WEAK")
        elif score <= 4:
            print("STRENGTH: 🟡 MEDIUM")
        else:
            print("STRENGTH: 🟢 STRONG")
            
        print(f"Score: {score}/5")
        
        if feedback:
            print("Tips to improve:")
            for tip in feedback:
                print(f" - {tip}")
        else:
            print("Great! This is a strong password.")

if __name__ == "__main__":
    main()
