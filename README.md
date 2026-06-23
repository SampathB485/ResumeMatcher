# Resume Matcher

An AI-powered resume analysis tool that scores your resume against any job description, identifies skill gaps, rewrites weak sections using LLMs, and exports a polished PDF built to demonstrate end-to-end Python backend and NLP pipeline development.

---

**Live Demo:** [resume-matcher-ashray.streamlit.app](https://resume-matcher-ashray.streamlit.app/)

---

## What it does

- Upload or paste your resume (PDF or plain text)
- Paste any job description
- Generates semantic embeddings and calculates a **Match Score (%)**
- Highlights missing skills and keywords the JD requires
- Uses an LLM (Gemini / Groq / OpenAI — configurable) to rewrite weak resume sections
- Generates likely interview questions based on the JD
- Exports a clean, formatted PDF of the improved resume

---

## Architecture

```
┌─────────────────────────────────────────────┐
│                  Streamlit UI               │
│              (app.py — frontend layer)      │
└────────────────────┬────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │     Core Pipeline     │
         ├───────────────────────┤
         │ resume_parser.py      │  Extract text from uploaded resume
         │ jd_parser.py          │  Parse and clean job description
         │ match_engine.py       │  Embedding generation + cosine similarity score
         │ gpt_writer.py         │  LLM rewrite of weak resume sections
         │ interview_questions.py│  Generate role-specific interview prep
         │ recruiter_tools.py    │  Keyword gap analysis + skill extraction
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │      Output Layer     │
         ├───────────────────────┤
         │ utils/pdf_export.py   │  ReportLab PDF generation
         └───────────────────────┘
```

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| UI framework | Streamlit |
| Embeddings | NumPy + cosine similarity |
| LLM APIs | Google Gemini / Groq / OpenAI (configurable) |
| PDF export | ReportLab |
| Text parsing | Regex, string processing |
| Secrets management | Streamlit secrets.toml |

---

## Local setup

```bash
# 1. Clone the repo
git clone https://github.com/AshraySikka/Resume-matcher.git
cd Resume-matcher

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
mkdir -p .streamlit
echo 'GEMINI_API_KEY = "your-key-here"' > .streamlit/secrets.toml

# 5. Run the app
streamlit run app.py
```

---

## Project structure

```
Resume-matcher/
├── app.py                  # Main Streamlit app entry point
├── match_engine.py         # Embedding + similarity scoring
├── resume_parser.py        # Resume text extraction
├── jd_parser.py            # Job description parsing
├── gpt_writer.py           # LLM-powered section rewriter
├── interview_questions.py  # Interview question generator
├── recruiter_tools.py      # Keyword gap + skill analysis
├── utils/                  # PDF export helpers
├── requirements.txt
└── .gitignore
```

---

## Why I built this

Job seekers often apply to roles without knowing how well their resume actually maps to the job description. This tool automates that gap analysis using semantic similarity going beyond simple keyword matching and uses an LLM to actively improve the resume rather than just flag problems.

Built as part of my transition into backend Python development, focusing on LLM API integration, modular pipeline design, and practical NLP tooling.

---

## Author

**Ashray Sikka** — Backend Developer (Python · MySQL · PostgreSQL)
[LinkedIn](https://www.linkedin.com/in/ashraysikka) · [GitHub](https://github.com/AshraySikka)
