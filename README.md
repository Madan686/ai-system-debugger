# AI System Debugger

AI System Debugger is a Flask-based AI-powered debugging assistant that analyzes software errors, stack traces, and runtime exceptions using a locally hosted LLM (Mistral via Ollama).

The system provides:
- Error categorization
- Root cause analysis
- Practical debugging steps
- Suggested commands/code fixes
- Persistent debugging history

---

# Features

- AI-powered error analysis using Ollama + Mistral
- Structured JSON-based AI response pipeline
- Error category classification
- Root cause detection
- Practical fix recommendations
- SQLite-based debugging history
- Dynamic frontend rendering using JavaScript
- Copy-to-clipboard command support
- Modular backend architecture

---

# Tech Stack

## Backend
- Python
- Flask
- SQLite

## Frontend
- HTML
- CSS
- JavaScript

## AI Integration
- Ollama
- Mistral LLM

---

# Project Structure

```text
ai-system-debugger/
│
├── app.py
├── ai_engine.py
├── database.py
├── requirements.txt
├── debug_history.db
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── README.md