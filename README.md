# Advanced Password Analyzer

### Detailed Information on Password Analyzer with GUI and Password Suggestions

#### Overview
This Advanced Password Analyzer project evaluates the strength of a password, detects weaknesses, checks against known compromised databases, calculates entropy, and provides actionable recommendations. The application features a clean, responsive graphical user interface (GUI) built with Python's Tkinter library.

#### Features
1. **Comprehensive Evaluation**: Analyzes passwords based on length, character variety (uppercase, lowercase, numbers, symbols).
2. **Entropy Calculation**: Calculates Shannon entropy to provide a mathematical measure of password unpredictability.
3. **Compromised Password Check**: Securely checks passwords against the Have I Been Pwned (HIBP) database using k-Anonymity (only the first 5 characters of the SHA-1 hash are sent).
4. **Real-time Feedback**: Provides instant visual feedback via a strength progress bar and detailed suggestions as you type.
5. **Secure Password Generation**: Generates cryptographically strong passwords tailored to meet all security criteria.
6. **User-Friendly GUI**: Clean interface with password visibility toggling and clear status indicators.

#### Project Structure
1. **Setup Python Environment**: Ensure all necessary packages are installed (`requests`, `tkinter`).
2. **Password Analyzer Logic**: Object-oriented backend (`PasswordAnalyzer` class) for robust analysis.
3. **Design the GUI**: Modernized Tkinter UI (`PasswordAnalyzerApp` class).
4. **Integration**: Seamless real-time updates linking the logic to the UI.

### Installation & Usage

#### 1. Setup Python Environment
Ensure you have Python 3 and Tkinter installed on your system.
You will also need the `requests` library for the compromised password checks.

- **Python & Tkinter Installation (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install python3 python3-tk python3-pip
  ```
- **Install Dependencies**:
  ```bash
  pip3 install requests
  ```

#### 2. Run the Application
Navigate to the project directory and run the script:
```bash
python3 pass_encrypt.py
```

### Security Note
The Have I Been Pwned API integration utilizes the k-Anonymity model. Your full password or full password hash is **never** sent over the internet. Only the first 5 characters of the SHA-1 hash are transmitted to the API, ensuring your password remains secure.
