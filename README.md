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

# How It Works

1. User submits an error log from the frontend  
2. Flask API receives and validates the request  
3. AI prompt is dynamically generated  
4. Ollama sends the request to the Mistral model  
5. AI returns structured JSON debugging analysis  
6. Backend stores results in SQLite database  
7. Frontend dynamically renders debugging insights and history  

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>
cd ai-system-debugger
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Install Ollama

Download Ollama:

https://ollama.com/download

Pull Mistral model:

```bash
ollama pull mistral
```

Start Ollama server:

```bash
ollama serve
```

---

# Run Application

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

# Example Errors

## Import Error

```text
ModuleNotFoundError: No module named 'flask'
```

---

## Database Error

```text
sqlite3.OperationalError: no such table: users
```

---

## Runtime Error

```text
ZeroDivisionError: division by zero
```

---

## API Error

```text
405 Client Error: Method Not Allowed
```

---

# API Endpoints

## Analyze Error

```http
POST /analyze
```

### Request

```json
{
  "error_text": "ModuleNotFoundError: No module named flask"
}
```

---

## Get History

```http
GET /history
```

---

# Future Improvements

- Multi-file debugging support  
- Source code upload and analysis  
- Framework-aware debugging  
- Search and filter history  
- Confidence score prediction  
- Error analytics dashboard  
- Docker deployment  
- User authentication system  

---

# Learning Outcomes

This project demonstrates:

- Flask backend development  
- REST API design  
- Prompt engineering  
- AI response structuring  
- Local LLM integration  
- SQLite database management  
- Dynamic frontend rendering  
- Frontend-backend communication  
- Layered software architecture  