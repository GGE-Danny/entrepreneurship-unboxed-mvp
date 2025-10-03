
# Entrepreneurship Unboxed – MVP (Flask)

Lightweight prototype for:
1) Investor matching (rule-based, optional ranking)
2) Founder dashboard (dummy health + next action)

## Quickstart

⚙️ Setup Instructions
1. Install Python

Download and install Python 3.x
.

During installation, ensure you check “Add Python to PATH”.

Verify install:
python --version

If you see Python was not found, disable Windows App Execution Aliases:

Go to Settings → Apps → Advanced app settings → App execution aliases

Turn off python.exe and python3.exe

2. VS Code Setup

Open the project in VS Code.

Press Ctrl+Shift+P → Python: Select Interpreter → choose the Python version you installed.

If you prefer Command Prompt instead of PowerShell inside VS Code (to avoid script execution issues):

Open VS Code terminal dropdown → select Command Prompt.

3. Create Virtual Environment

From project root:
python -m venv .venv


Activate it!!! :-

Windows (cmd):
.venv\Scripts\activate.bat


PowerShell (if allowed):
.venv\Scripts\activate


macOS/Linux:
source .venv/bin/activate

4. Install Dependencies:
pip install -r requirements.txt

5. Run the App:
python app.py

summary: 
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open:
- Home: http://127.0.0.1:5000/
- Dashboard UI: http://127.0.0.1:5000/dashboard

## API
FOR MATCHING:
**POST /match?rank=true|false**

Body:
```json
{ "industry": "Fintech", "stage": "Seed", "min_funding": 100000, 
  "max_funding": 500000  }
```

Response:
```json
{ "ok": true,
  "ranked": true,
  "matches": [
    {
      "name": "Seed Ventures",
      "industry": "Fintech",
      "stage": "Seed",
      "min_investment": 50000,
      "max_investment": 500000,
      "score": 0.92
    }
  ] }
```

**GET /investors** → returns dummy investors.

## Assumptions
- Dummy JSON dataset (no DB)
- No authentication (MVP)
- Rule-based matching; optional simple ranking for bonus
- fluid range for funding amount

## Known Limitations
- Not secure
- No pagination or advanced filters
- In-memory dataset
- No KYC 
- No Authorization

