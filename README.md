# 🔐 SSO Detection (Google SSO)

This Python tool scans a list of subdomains and detects whether **Google SSO (Single Sign-On)** is implemented on the login page.  
It uses **Playwright** for browser automation and handles multiple redirections to catch deeper SSO integrations.

---

## 📌 Features

- Automatically adds `https://` to domains if missing.
- Handles multiple redirects and dynamically rendered content.
- Detects:
  - Visible text like `Sign in with Google`, `Login with Google`, etc.
  - Redirects to `accounts.google.com`
- Clean output with titles of pages and SSO status.
- Ignores technical stack traces – only prints `Error Occurred` for failures.

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/sso-detection-tool.git
cd sso-detection-tool

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Use venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

## 📄 Usage

1. **Prepare `subdomains.txt`**

List one domain per line:
admin.example.com
auth.example.com
portal.example.org

2. **Run the script**

```bash
python sso_check.py

## 📋 Requirements

Python 3.7+
Playwright
BeautifulSoup



