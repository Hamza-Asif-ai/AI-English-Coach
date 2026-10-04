# 🎓 AI English Coach — Level-Based English Practice & Instant AI Feedback

An AI-powered English learning platform built on **CrewAI multi-agent generation**. Pick a level (**Beginner / Intermediate / Advanced**) and a skill (**Reading / Writing / Vocabulary / Grammar**) and four specialist agents generate a fresh, level-appropriate exercise every time — **10 validated multiple-choice questions** per quiz, or a writing task with detailed AI feedback, a score out of 10 and a corrected version. Every result is saved to a progress dashboard with streaks, per-skill averages and a "Coach recommends" hint.

![Python](https://img.shields.io/badge/Python-3.10--3.13-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)
![React](https://img.shields.io/badge/Frontend-React%2019-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Build-Vite-646CFF?logo=vite&logoColor=white)
![Tailwind](https://img.shields.io/badge/Style-Tailwind%20CSS%204-06B6D4?logo=tailwindcss&logoColor=white)
![CrewAI](https://img.shields.io/badge/Agents-CrewAI-FF5A50)
![Groq](https://img.shields.io/badge/LLM-Groq%20(gpt--oss--20b)-F55036)
![Pydantic](https://img.shields.io/badge/Validation-Pydantic-E92063?logo=pydantic&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?logo=render&logoColor=white)
![Theme](https://img.shields.io/badge/Theme-Light%20%2F%20Dark-lightgrey)

> 🌐 **Live Demo:** see the [Live Demo](https://ai-english-coach-ruddy.vercel.app/)) section below for the public URL.

<!--
Optional: add a live-demo badge once you have your public URL, for example:
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-brightgreen?logo=render&logoColor=white)](https://YOUR-FRONTEND-URL.onrender.com)
-->

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Live Demo](#-live-demo)
- [Technology Stack](#-technology-stack)
- [Practice Modules](#-practice-modules)
- [Difficulty Levels](#-difficulty-levels)
- [Pipeline Architecture](#-pipeline-architecture)
- [Question Quality Design](#-question-quality-design)
- [Configuration](#-configuration)
- [Testing & Validation](#-testing--validation)
- [System Architecture](#-system-architecture)
- [How to Run](#-how-to-run)
- [Deployment on Render](#-deployment-on-render)
- [Project Structure](#-project-structure)
- [Calibration & Tuning](#-calibration--tuning)
- [Known Limitations](#-known-limitations)
- [Troubleshooting](#-troubleshooting)
- [Real-World Applications](#-real-world-applications)
- [Author](#-author)

---

## 📌 Project Overview

Static worksheets and fixed question banks run out quickly, ignore the learner's level, and give no feedback on writing. AI English Coach closes those gaps:

1. **Quiz Engine** — for Reading, Vocabulary and Grammar, a dedicated CrewAI agent writes a brand-new exercise with **10 multiple-choice questions** whose type and difficulty change with the selected level. Every AI reply is validated (4 distinct options, exactly one correct letter, no duplicate questions) before it ever reaches the screen.
2. **Writing Engine** — a writing agent creates a level-appropriate task, then marks the learner's answer: a **score out of 10**, feedback on grammar, vocabulary, spelling/punctuation and structure, strengths, improvements, a **corrected version** and a tip.
3. **Progress Engine** — each result is stored anonymously (no login) and turned into practice counts, average score, day streak, per-skill averages and a recommendation for what to practise next.

### 🎯 Objectives

- Generate a fresh exercise on every click — a random theme / grammar point is injected into each prompt, so exercises do not repeat
- Ask **10 logical, technically correct questions** per Reading, Vocabulary and Grammar practice, with plausible but definitely-wrong distractors
- Match question **type and difficulty to the level** (Beginner, Intermediate, Advanced) — not just the vocabulary of the passage
- Give writing feedback that is fair for the learner's level, quotes the real mistakes and returns a fully correct rewrite
- Never show broken data: **Pydantic validation + automatic retry** guarantee that the frontend only receives clean exercises
- Keep generation fast with a low-reasoning model setting and a capped output length
- Offer a comfortable study experience with a **light / dark theme** switch

---

## 🌐 Live Demo

<!--
Replace the placeholder URLs below with your real Render URLs after deployment.
-->

| Service | URL |
|---|---|
| 🖥️ **Web App (Frontend)** | `https://YOUR-FRONTEND-URL.onrender.com` |
| ⚙️ **Backend API** | `https://YOUR-BACKEND-URL.onrender.com` |
| 📖 **Interactive API Docs** | `https://YOUR-BACKEND-URL.onrender.com/docs` |
| ❤️ **Health Check** | `https://YOUR-BACKEND-URL.onrender.com/api/health` |

> ⏱️ If the backend runs on a free hosting plan, it may go to sleep when idle. The first request after a pause can take about a minute while the server wakes up.

<!--
Optional: add screenshots here once they are saved in docs/screenshots/
![Home – light theme](docs/screenshots/home-light.png)
![Quiz – dark theme](docs/screenshots/quiz-dark.png)
-->

---

## 🧰 Technology Stack

| Component | Technology |
|---|---|
| Frontend | React 19 + Vite + Tailwind CSS 4 |
| Backend API | FastAPI + Uvicorn |
| Multi-Agent Layer | CrewAI — four specialist agents (Reading, Writing, Vocabulary, Grammar), each run as Agent → Task → Crew |
| LLM | Groq (`openai/gpt-oss-20b` by default, any Groq model id works) through CrewAI / LiteLLM |
| Output Validation | Pydantic v2 — strict schemas with tolerant key names, option cleaning and question de-duplication |
| Database | SQLite (anonymous `client_id`, no login) |
| Theme | Light / Dark switch, saved in the browser and applied before first paint |
| Testing | pytest (real CrewAI Agent/Task/Crew with a fake LLM — no API key needed) + ESLint |
| Deployment | Render (Web Service for the API, Static Site for the frontend) |
| Language | Python 3.10 – 3.13, JavaScript (ES modules) |

---

## 🎓 Practice Modules

| Module | What the learner gets |
|---|---|
| 📖 **Reading** | An original passage on a random theme + **10 questions** (facts, meaning in context, cause and effect, inference, author's tone — depending on the level) |
| ✍️ **Writing** | A clear writing task (text type, 2–4 points to cover, recommended length), then **AI feedback**: score /10, grammar, vocabulary, spelling & punctuation, structure, strengths, improvements, corrected version and a tip |
| 📚 **Vocabulary** | One new word with meaning, part of speech, example and synonyms, followed by **10 quiz questions** (meaning, word in a sentence, synonyms/opposites, collocations, word forms) |
| 📝 **Grammar** | A short rule explanation on a random grammar point for the level, followed by **10 questions** (fill in the blank, correct sentence, error spotting, sentence transformation) |

### 🖥️ Quiz screen

- **Question navigator** — numbered buttons 1–10; answered questions turn green, so the learner can jump around freely
- **Submit guard** — the last screen lists which questions are still unanswered
- **Result review** — every question shows the learner's answer, the correct answer and a short explanation
- **Light / Dark theme** — one-click toggle in the header; the choice is remembered, and the first visit follows the system setting

### 📈 Progress dashboard

| Metric | Meaning |
|---|---|
| Practices | Total number of completed practices |
| Average score | Mean percentage across all results |
| Day streak | Consecutive practice days (today or yesterday counts) |
| Per-skill average | Count and average per Reading / Writing / Vocabulary / Grammar |
| ⭐ Coach recommends | The first skill not tried yet, otherwise the weakest skill |

---

## 🚦 Difficulty Levels

Level changes **both** the language and the type of question.

| Aspect | Beginner (A1–A2) | Intermediate (B1–B2) | Advanced (C1–C2) |
|---|---|---|---|
| Passage length | 80–110 words | 130–180 words | 160–220 words |
| Writing length | 40–60 words | 100–150 words | 180–250 words |
| Reading questions | Stated facts, common-word meaning, simple "what is it about" | Detail, cause/effect, meaning from context, reference, simple inference | Inference, author's purpose and tone, subtle word choice, main idea, "NOT supported" question |
| Vocabulary questions | Meaning, simple synonym/opposite, word form | Meaning in context, collocations, word forms | Near-synonym nuance, connotation, spotting wrong usage |
| Grammar topics | Present/past simple, articles, prepositions, comparatives… | Present perfect, conditionals, reported speech, passive, relative clauses… | Third/mixed conditionals, inversion, cleft sentences, participle clauses, subjunctive… |
| Writing task | Familiar topics, simple sentences | Explain or give an opinion with reasons and examples | Argue, evaluate or compare in a formal register |
| Distractors | Clearly wrong but reasonable | Believable | All four options look plausible |

---

## 🤖 Pipeline Architecture

### Exercise generation (Reading / Vocabulary / Grammar / Writing task):
```
Area + Level
→ Prompt Builder (level guide + question mix + quality rules + random theme/topic + JSON-only rules)
→ CrewAI: Specialist Agent → Task → Crew (Groq LLM, low reasoning effort, capped tokens)
→ JSON Extraction (tolerates code fences / extra text)
→ Pydantic Validation (10 valid, different questions · 4 distinct options · one correct letter)
→ ✅ valid  → exercise returned to the frontend
→ ❌ invalid → retry (up to 3 attempts) with the exact error added to the prompt
→ still invalid → clear 502 error: "please try again"
```

### Writing evaluation:
```
Student text (wrapped in <student_text> tags = treated as data, never as instructions)
→ Writing Agent marks it with a level-aware score guide
→ Pydantic Validation (score clamped to 0–10, lists must be non-empty)
→ score + feedback + corrected version → frontend
```

### Progress:
```
Quiz submitted / writing marked → POST /api/progress (client_id, area, level, score, total)
→ SQLite → streak · averages · per-skill stats · "Coach recommends"
```

---

## 🎯 Question Quality Design

A wrong "correct answer" is the worst mistake a learning app can make. Several layers protect against it:

| Layer | What it does |
|---|---|
| **Quality rules in every quiz prompt** | Questions must be logical and technically correct English; the right option must be provable from the passage, the grammar rule or the dictionary meaning |
| **One correct option only** | Each wrong option must be wrong for a clear reason (wrong meaning, wrong form/tense, contradicts the text, or not stated) — never two acceptable answers |
| **Distractor discipline** | Same kind and similar length as the right answer; no joke options; **no** "all/none of the above" or "both A and B"; the correct option is never longer than the others |
| **Level-specific question mix** | The prompt lists exactly which question types to use at each level for each skill |
| **Self-check instruction** | The model is told to verify every answer letter before replying and to spread the correct letters (A–D) evenly |
| **Schema validation** | 4 distinct options (case-insensitive, punctuation counts), valid answer letter, vague options rejected, duplicate questions removed |
| **Spare-question buffer** | The AI writes 11 questions and the first 10 valid, different ones are kept — one broken question does not fail the whole exercise |
| **Option cleaning** | Leading `A.` / `B)` prefixes added by the model are stripped; list-style options and answer text are mapped to letters |
| **Retry loop with feedback** | An invalid reply is retried (up to 3 times) with the exact validation error included in the prompt |
| **Writing feedback rules** | Fair score guide (9–10 … 0–2), only real mistakes are reported with the student's own words quoted, and the corrected version must itself be correct |
| **Prompt-injection protection** | Student text is wrapped in tags and the agent is told never to follow instructions inside it |

---

## 🔧 Configuration

### Backend (`backend/.env`)

| Setting | Default | Why |
|---|---|---|
| `GROQ_API_KEY` | — | **Required.** Free key from [console.groq.com/keys](https://console.groq.com/keys) |
| `GROQ_MODEL` | `openai/gpt-oss-20b` | Any Groq model id (a leading `groq/` is removed automatically) |
| `GROQ_REASONING_EFFORT` | `low` | How long the model "thinks" before answering. `low` is fastest; `medium` / `high` are slower but deeper. Only applies to `gpt-oss` models |
| `LLM_MAX_TOKENS` | `5000` | Caps the length of each AI reply (keeps generation quick, still fits 11 questions) |
| `LLM_TIMEOUT` | `90` | Seconds per AI call |
| `LLM_MAX_ATTEMPTS` | `3` | Retries when the AI returns an invalid reply |
| `CORS_ORIGINS` | — | Comma-separated frontend URLs allowed to call the API (needed after deployment) |
| `DATABASE_PATH` | `backend/data/progress.db` | SQLite file location |
| `CREW_VERBOSE` | `false` | Show CrewAI agent logs in the terminal |

### Frontend (`frontend/.env`)

| Setting | Default | Why |
|---|---|---|
| `VITE_API_URL` | empty | Leave empty in development (Vite proxies `/api` to `127.0.0.1:8000`). Set to the backend URL when the frontend is deployed separately |

### Built-in defaults (`backend/app/`)

| Setting | Value | File |
|---|---|---|
| Questions shown per quiz | 10 | `prompts.py` + `schemas.py` |
| Spare questions requested | 1 (11 asked, 10 kept) | `prompts.py` |
| LLM temperature | 0.6 | `llm.py` |
| Writing answer length | 10 – 6000 characters | `schemas.py` |
| Allowed levels / skills | Beginner, Intermediate, Advanced / Reading, Writing, Vocabulary, Grammar | `schemas.py` |

---

## 📊 Testing & Validation

| Test | Method | Result |
|---|---|---|
| MCQ normalisation | List-style options, answer text ("three"), `b. glad`, lowercase letters (`tests/test_schemas.py`) | Mapped to a clean A–D structure |
| Option prefixes | Options such as `A. sad`, `B) glad`, `C: angry` | Prefix removed, real text kept |
| Duplicate / vague options | Same text in two options, `SAD` vs `sad`, "All of the above" | Rejected by validation |
| Punctuation-only options | Grammar options that differ by a comma or semicolon | Accepted as different, valid options |
| 10-question rule | Reading, Vocabulary and Grammar with 9, 10 and 11 questions | 9 rejected, 11 trimmed to 10 |
| Spare-question buffer | 11 questions where one has duplicate options | Broken one dropped, 10 returned |
| Duplicate questions | The same question repeated 10 times | Rejected |
| Writing feedback | Score as `"8/10"`, `14`, `6.6` | Parsed and clamped to 0–10 |
| JSON extraction | Plain JSON, code fences, extra text around JSON, non-JSON, JSON arrays | Correct object or a clean error |
| API — every area | `/api/generate-exercise` for all four skills (`tests/test_api.py`) | 200 with a validated exercise |
| API — error paths | Unknown area/level, missing API key, AI exception, AI keeps failing | 422 / 503 / 502 with clear messages |
| Retry logic | Invalid first reply, valid second reply | Succeeds on the second attempt; exhausted retries return 502 |
| Progress & recommendation | Save results, read stats, weakest-area logic, input validation | Correct averages, streak, recommendation; bad input → 422 |
| CORS | Preflight from `http://localhost:5173` | Allowed |
| CrewAI wiring | Real Agent/Task/Crew with a fake LLM (`tests/test_crew_wiring.py`) | Prompt reaches the model un-mangled, even with `{curly braces}` in student text |

Run the backend suite (no API key or internet needed):
```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest
```

Frontend checks:
```bash
cd frontend
npm run lint
npm run build
```

---

## 🧱 System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│          React 19 + Vite + Tailwind CSS 4  (single page app)      │
│  Level picker · Skill cards · Quiz / Writing screens · Progress   │
│               Light / Dark theme toggle (saved locally)           │
└───────────────────────────────┬──────────────────────────────────┘
                                │  HTTPS / JSON   (/api/...)
                         FastAPI (CORS)
              ┌─────────────────┴──────────────────┐
              │                                    │
   /api/generate-exercise                    /api/progress
   /api/evaluate-writing                     (save + stats)
              │                                    │
      services.py: Agent → Task → Crew             │
      (retry + Pydantic validation)           SQLite (results)
              │
      CrewAI agents (Reading · Writing · Vocabulary · Grammar)
              │
         Groq LLM (gpt-oss-20b)
```

---

## 🚀 How to Run

You need **two terminals** — one for the backend and one for the frontend.

**Requirements:** Python 3.10 – 3.13 (CrewAI does not support 3.14 yet), Node.js 20+, and a free [Groq API key](https://console.groq.com/keys).

### 1️⃣ Backend

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

Open `backend/.env` and paste your key: `GROQ_API_KEY=gsk_...`

Start the server:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Check it at **http://127.0.0.1:8000/api/health** (interactive docs at **/docs**).

### 2️⃣ Frontend

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**.

### 🔌 REST API

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Status and whether `GROQ_API_KEY` is set |
| `/api/generate-exercise` | POST | `{ "area": "Grammar", "level": "Advanced" }` → a validated exercise (10 questions for Reading, Vocabulary, Grammar) |
| `/api/evaluate-writing` | POST | `{ level, topic, instructions, answer }` → score, feedback and corrected version |
| `/api/progress` | POST | Save a result `{ client_id, area, level, score, total }` and get updated stats |
| `/api/progress?client_id=...` | GET | Progress stats and recommendation |

---

## ☁️ Deployment on Render

The project deploys as **two services**: the FastAPI backend as a *Web Service* and the React frontend as a *Static Site*. Deploy the backend first, because the frontend needs its URL.

### Backend — Web Service

| Field | Value |
|---|---|
| Root Directory | `backend` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/api/health` |

Environment variables:

| Variable | Value |
|---|---|
| `PYTHON_VERSION` | `3.12.8` (any 3.12.x — CrewAI does not support Python 3.14 yet) |
| `GROQ_API_KEY` | your Groq key |
| `CORS_ORIGINS` | your frontend URL (add this after the frontend is created, no trailing `/`) |

### Frontend — Static Site

| Field | Value |
|---|---|
| Root Directory | `frontend` |
| Build Command | `npm install && npm run build` |
| Publish Directory | `dist` |

Environment variable: `VITE_API_URL` = your backend URL (no trailing `/`).

### Finishing up

1. Copy the frontend URL into the backend's `CORS_ORIGINS` and let the backend redeploy.
2. Open `<backend-url>/api/health` — it should return `"status": "healthy"` and `"llm_configured": true`.
3. Open the frontend URL and try every skill at every level.
4. Add both URLs to the [Live Demo](#-live-demo) section.

> **Notes:** `VITE_API_URL` is baked in at build time — after changing it, redeploy the frontend with *Clear build cache & deploy*. CrewAI is a large library, so serverless functions are not a good fit; use a normal web service. On a free plan the memory is small and the disk is temporary, so SQLite progress can reset on restart — use a paid instance with a persistent disk if you want progress to survive.

---

## 📁 Project Structure

```
ai-english-coach/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   └── screenshots/                # App screenshots (light + dark)
├── backend/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pytest.ini
│   ├── .env.example                # Copy to .env and add GROQ_API_KEY
│   ├── data/                       # SQLite database (git-ignored)
│   ├── tests/
│   │   ├── conftest.py             # Isolated env: no real key, temp database
│   │   ├── samples.py              # Canned AI replies used by the tests
│   │   ├── test_api.py             # Endpoints, errors, retries, progress, CORS
│   │   ├── test_crew_wiring.py     # Real Agent/Task/Crew with a fake LLM
│   │   └── test_schemas.py         # MCQ rules, 10-question rule, JSON extraction
│   └── app/
│       ├── main.py                 # FastAPI app, CORS, startup
│       ├── routes.py               # /api endpoints
│       ├── agents.py               # 4 CrewAI agents (Reading, Writing, Vocabulary, Grammar)
│       ├── prompts.py              # Level guides, question mix, quality rules, themes
│       ├── services.py             # Agent → Task → Crew, JSON extraction, validation, retries
│       ├── schemas.py              # Pydantic models for requests and AI output
│       ├── db.py                   # SQLite progress + coach recommendation
│       ├── llm.py                  # Groq LLM setup (reasoning effort, token cap)
│       └── config.py               # Environment settings
└── frontend/
    ├── index.html                  # Applies the saved theme before first paint
    ├── package.json
    ├── vite.config.js              # Dev proxy: /api → http://127.0.0.1:8000
    ├── eslint.config.js
    ├── .env.example
    ├── public/
    │   └── favicon.svg
    └── src/
        ├── main.jsx
        ├── App.jsx                 # State, API calls, theme toggle
        ├── api.js                  # fetch wrapper + anonymous client id
        ├── index.css               # Tailwind import + dark-theme styles
        └── components/
            ├── LevelSelection.jsx  # Beginner / Intermediate / Advanced
            ├── AreaCards.jsx       # The four skill cards
            ├── QuizPractice.jsx    # 10-question quiz, navigator, result review
            ├── WritingPractice.jsx # Writing task + AI feedback
            └── ProgressPanel.jsx   # Stats, per-skill bars, recommendation
```

---

## 📐 Calibration & Tuning

- **Exercises feel too easy or too hard** — edit `QUESTION_MIX` and `QUESTION_DIFFICULTY` in `backend/app/prompts.py`; they control the question types and distractor strength for each level.
- **Want more variety** — extend the `THEMES` and `GRAMMAR_TOPICS` lists in `prompts.py`.
- **Generation is slow** — keep `GROQ_REASONING_EFFORT=low`, lower `LLM_MAX_TOKENS` carefully, or set `EXTRA_QUESTIONS = 0` in `prompts.py` (fewer questions to write, but one broken question will then trigger a retry).
- **Too many "AI could not produce a valid result" errors** — raise `LLM_MAX_ATTEMPTS`, or try `GROQ_REASONING_EFFORT=medium` for more careful answers.
- **Change the number of questions** — update `QUESTION_COUNT` in **both** `prompts.py` and `schemas.py` (keep them equal) and adjust the card text in `AreaCards.jsx`.
- **Dark theme colours** — all dark-mode colours live in `frontend/src/index.css`.
- **Use another Groq model** — set `GROQ_MODEL`; `reasoning_effort` is only sent to `gpt-oss` models.

---

## 🚧 Known Limitations

- **AI-generated content can still contain mistakes.** Prompts, validation and retries reduce errors a lot, but no automatic check can prove every question and answer is correct; treat the app as a practice aid, not an official exam.
- **Writing scores are AI estimates.** They are consistent with a score guide but are not a certified assessment.
- **No accounts.** Progress is tied to an anonymous id stored in the browser; clearing site data or switching browser starts a new history.
- **SQLite on temporary storage.** On hosts without a persistent disk, progress is lost when the server restarts.
- **Groq free-tier limits.** Heavy use can hit rate limits (HTTP 429), which appear as a "please try again" message.
- **Cold starts on free hosting.** The first request after idle time can take about a minute.
- **Python version.** CrewAI currently requires Python 3.10 – 3.13.
- **Text-only practice.** There is no speaking or listening module yet.

---

## 🩺 Troubleshooting

| Problem | Solution |
|---|---|
| "Cannot reach the backend" | The backend is not running on port 8000 (local), or `VITE_API_URL` points to the wrong URL (deployed) |
| "GROQ_API_KEY is not set" (503) | Create `backend/.env` from `.env.example`, add your key, restart the backend |
| "The AI could not produce a valid result… try again" (502) | The model's reply failed validation three times. Click **Try Again**; if it repeats, raise `LLM_MAX_ATTEMPTS` or use `GROQ_REASONING_EFFORT=medium` |
| Slow first exercise | A normal AI call takes several seconds; Advanced and 10-question quizzes take longer. Keep `GROQ_REASONING_EFFORT=low` |
| HTTP 429 / rate limit from Groq | Free-tier quota reached — wait a minute, or use a paid key |
| `pip install` fails on Python 3.14 | Use Python 3.12 or 3.13 |
| CORS error in the browser after deploying | Set `CORS_ORIGINS` on the backend to the exact frontend URL (no trailing `/`) and redeploy |
| Frontend still calls the old backend URL | `VITE_API_URL` is applied at build time — rebuild the frontend |
| Progress disappeared on Render | Free instances have temporary disk; use a persistent disk or a paid plan |
| First request is very slow on Render | A free instance was asleep; it needs about a minute to wake |
| Dark theme looks wrong after an update | Hard-refresh the page (Ctrl + Shift + R) so the new `index.css` loads |

---

## 🌍 Real-World Applications

- **Self-learners** — unlimited, level-matched English practice with instant feedback
- **Schools and tutoring centres** — extra homework practice that never repeats
- **Exam and IELTS-style preparation** — reading, vocabulary, grammar and writing drills on demand
- **Corporate language training** — a lightweight practice layer for employees improving workplace English
- **Teachers** — a fast source of fresh reading passages and quiz questions at the right level
- **Developers** — a clean reference for CrewAI + FastAPI + React with validated structured LLM output

---

## 👨‍💻 Author

**Hamza Asif**  
BS Artificial Intelligence — DUET, Karachi

[![GitHub](https://img.shields.io/badge/GitHub-Hamza--Asif--ai-black?style=flat-square&logo=github)](https://github.com/Hamza-Asif-ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Hamza%20Asif-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/hamza-asif-ai)

---
