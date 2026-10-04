# 🎓 AI English Coach

An AI-powered English learning app. Choose a level (Beginner / Intermediate / Advanced)
and a skill, and **CrewAI agents** generate a fresh exercise every time:

| Skill | What you get |
|---|---|
| 📖 Reading | A passage + 5 multiple-choice questions |
| ✍️ Writing | A writing task, then detailed AI feedback, a score out of 10 and a corrected version |
| 📚 Vocabulary | A new word with meaning, example, synonyms and a quiz question |
| 📝 Grammar | A grammar rule and a quiz question |

Your results are saved (SQLite) and shown as a progress dashboard: practices, average score,
day streak, per-skill averages and a "Coach recommends" hint for what to practise next.

**Stack:** React 19 + Vite + Tailwind CSS 4 · FastAPI · CrewAI · Groq (`openai/gpt-oss-20b`) · SQLite

## Project structure

```
ai-english-coach/
├── backend/
│   ├── app/
│   │   ├── main.py        FastAPI app, CORS, startup
│   │   ├── routes.py      /api endpoints
│   │   ├── agents.py      4 CrewAI agents (Reading, Writing, Vocabulary, Grammar)
│   │   ├── prompts.py     prompts (level, random theme, JSON format)
│   │   ├── services.py    runs Agent -> Task -> Crew, validates JSON, retries
│   │   ├── schemas.py     Pydantic models for requests and AI output
│   │   ├── db.py          SQLite progress + coach recommendation
│   │   ├── llm.py         Groq LLM setup
│   │   └── config.py      environment settings
│   ├── tests/             28 automated tests (no API key needed)
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/               App.jsx, api.js, components/
    ├── vite.config.js     dev proxy: /api -> http://127.0.0.1:8000
    └── package.json
```

## Requirements

- **Python 3.10 – 3.13** (CrewAI does not support 3.14 yet)
- **Node.js 20+**
- A free **Groq API key**: https://console.groq.com/keys

## Setup and run

You need two terminals: one for the backend and one for the frontend.

### 1. Backend

Windows (PowerShell):

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

macOS / Linux:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Open `backend/.env` and put your key: `GROQ_API_KEY=gsk_...`

Start the server:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Check it: http://127.0.0.1:8000/api/health (interactive docs: http://127.0.0.1:8000/docs)

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Status and whether `GROQ_API_KEY` is set |
| POST | `/api/generate-exercise` | `{ "area": "Reading", "level": "Beginner" }` returns a validated exercise |
| POST | `/api/evaluate-writing` | `{ level, topic, instructions, answer }` returns score + feedback |
| POST | `/api/progress` | Save a result `{ client_id, area, level, score, total }`, returns updated stats |
| GET | `/api/progress?client_id=...` | Progress stats |

## How reliability is handled

- The AI is asked for **one JSON object**; the backend validates it with Pydantic
  (exactly 5 reading questions, 4 distinct options A–D, one valid answer letter, ...).
- If the reply is invalid, the backend **retries** (up to 3 attempts, configurable) with the error
  included in the prompt. The frontend only ever receives clean, validated data.
- Every request gets a random theme / grammar topic, so exercises do not repeat.
- Student text is wrapped in tags and treated as data (basic prompt-injection protection).
- Clear errors: missing key → 503 with instructions, AI failure → 502, bad input → 422.

## Tests

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest
```

The tests run the real CrewAI Agent/Task/Crew with a fake LLM, so no API key or internet is needed.
Frontend checks: `cd frontend && npm run lint && npm run build`.

## Configuration (`backend/.env`)

| Variable | Default | Meaning |
|---|---|---|
| `GROQ_API_KEY` | – | Required for generating exercises |
| `GROQ_MODEL` | `openai/gpt-oss-20b` | Any Groq model id |
| `LLM_TIMEOUT` | `90` | Seconds per AI call |
| `LLM_MAX_ATTEMPTS` | `3` | Retries for invalid AI replies |
| `CORS_ORIGINS` | – | Comma-separated extra allowed origins (for deployment) |
| `DATABASE_PATH` | `backend/data/progress.db` | SQLite file location |
| `CREW_VERBOSE` | `false` | Show CrewAI agent logs in the terminal |

## Deployment notes

- **Frontend** (Vercel / Netlify): set `VITE_API_URL` to your backend URL, build with `npm run build`.
- **Backend** (Render / Railway / a VPS): run `uvicorn app.main:app --host 0.0.0.0 --port $PORT`,
  set `GROQ_API_KEY` and `CORS_ORIGINS=https://your-frontend-url`. CrewAI is large, so serverless
  functions are not a good fit. Use a normal server and a persistent disk for the SQLite file.

## Troubleshooting

- **"Cannot reach the backend"** – the backend is not running on port 8000.
- **"GROQ_API_KEY is not set"** – create `backend/.env` from `.env.example` and restart uvicorn.
- **Slow first exercise** – the AI call can take 10–40 seconds; the UI shows a loading card.
- **`pip install` fails on Python 3.14** – use Python 3.12 or 3.13.
- Never commit `.env`; it is already in `.gitignore`.
