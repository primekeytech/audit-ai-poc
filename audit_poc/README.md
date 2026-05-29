# Audit AI — POC
## AI-Powered Bank Audit Automation — Phase 1

---

## What This Does
This tool automates the bank IT audit workflow:
1. Upload bank documents (PDF, DOCX, XLSX)
2. Upload questionnaire responses
3. AI reads and analyses everything locally
4. Auto-populates work program columns F, G, H
5. Scores each control 1-4
6. Generates branded PDF report

---

## Setup Instructions

### Step 1 — Install Python
Download Python 3.11+ from python.org

### Step 2 — Install Ollama
Download from ollama.com
Then run:
```
ollama pull llama3
```
### Step 3 — Clone the repo
```
git clone https://github.com/primekeytech/audit-ai-poc
cd audit-ai-poc/audit_poc
```
### Step 4 — Install dependencies
```
pip install -r requirements.txt
```
### Step 5 — Add work program template
Copy Benjamin's template.xlsx into the workbook/ folder

### Step 6 — Run the app
```
streamlit run app.py
```
Browser opens automatically at http://localhost:8501

---

## Folder Structure
```
audit_poc/
├── app.py                 # Main Streamlit UI
├── config.yaml            # All settings here
├── requirements.txt       # Python dependencies
├── core/
│   ├── extractor.py       # PDF/DOCX/XLSX reading
│   ├── ai_provider.py     # AI abstraction layer
│   ├── workbook_engine.py # Excel population
│   └── report_engine.py   # PDF report generation
├── providers/
│   ├── ollama_provider.py # Local AI (Phase 1)
│   └── openai_provider.py # Future use
├── templates/
│   └── report.html        # Branded report template
├── workbook/
│   └── template.xlsx      # Benjamin's work program
└── outputs/               # Generated files saved here
```
---

## Switching AI Provider
Edit config.yaml:
```
ai:
provider: "ollama"    # Change to "openai" for OpenAI
```
---

## Important Notes
- NEVER modify workbook/template.xlsx directly
- All generated files saved to outputs/ folder
- AI suggests scores — always review before finalising
- Runs 100% locally — no internet required after setup

---

## Built By
Prime Key Software Solutions
contact@primekeytech.com
www.primekeytech.com
