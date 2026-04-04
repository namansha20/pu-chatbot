# PU-Chatbot: Implementation Overview

## Project Summary
- AI-powered chatbot for **Poornima University** to answer student queries
- Dual-component Python web application: **FastAPI backend** + **Streamlit frontend**
- Uses **TF-IDF + cosine similarity** (scikit-learn) for question matching — no generative AI
- Knowledge base stored in an Excel file (`pu_chatbot.xlsx`) with Question/Answer pairs
- Deployed on **Cloud Foundry (IBM SAP BTP)** with two separate application instances

---

## Architecture

- **Frontend (app/):** Streamlit web UI — handles user input and displays answers
- **Backend (srv/):** FastAPI REST API — processes questions and returns matched answers
- **Data Layer:** Excel file (`pu_chatbot.xlsx`) loaded into memory on each request
- **Communication:** Frontend calls backend via `POST /ask` with a JSON payload
- **Environment Config:** `PU_CHATBOT_API_URL` env variable configures the backend URL

---

## Backend (`srv/app.py`)

- Built with **FastAPI** and served using **Uvicorn** (ASGI)
- **`PoornimaUniversityBot` class** encapsulates all chatbot logic:
  - `getDataFrame(file_path)` — reads Excel dataset, drops null rows, resets index
  - `process_questions(user_input, data_frame)` — TF-IDF vectorization + cosine similarity matching
- **Endpoints:**
  - `POST /ask` — accepts `{"input": {"question": "..."}}`, returns `{"answer": "..."}`
  - `GET /` — health check with API description
- **File discovery:** looks for `pu_chatbot.xlsx` in current dir, then parent dir
- **Error handling:** catches missing file, empty dataset, and no-match scenarios

---

## Frontend (`app/app.py`)

- Built with **Streamlit** (356 lines)
- Custom CSS with modern gradient UI, glassmorphism effects, and fade-in animations
- **Font:** Playfair Display + DM Sans; **Color:** `#2563eb` (primary blue)
- **UI Sections:**
  - Branded hero banner with Poornima University title
  - Text input for user questions with example placeholders
  - Answer display box with formatted styling
  - University statistics panel (50+ Programs, 15K+ Students, 500+ Faculty, 98% Placement)
  - Footer with link to `poornima.edu.in`
- Calls backend API with a **30-second timeout**; handles connection errors and HTTP errors gracefully
- Backend URL defaults to the production Cloud Foundry URL; overridable via `PU_CHATBOT_API_URL`

---

## Data & NLP Pipeline

- **Dataset:** `pu_chatbot.xlsx` — Excel file with `Question` and `Answer` columns
- **No traditional database** — entire dataset loaded into pandas DataFrame on each API call
- **Matching pipeline:**
  1. Load all questions from the dataset
  2. Append the user's question to the list
  3. Apply `TfidfVectorizer` with English stop words
  4. Compute **cosine similarity** between the user question and all dataset questions
  5. Return the answer from the most similar match
- **Preprocessing:** null rows are dropped; index is reset for consistent access

---

## Deployment

- Configured via **`manifest.yml`** for Cloud Foundry
- Two CF applications deployed independently:
  - `pu-chatbot-api` → `cd srv && uvicorn app:app --host 0.0.0.0 --port $PORT`
  - `pu-chatbot-ui` → `cd app && streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Each app allocated **512MB memory** with random route assignment
- Python buildpack used for both applications

---

## Dependencies

| Package | Purpose |
|---|---|
| `fastapi` | Backend REST API framework |
| `uvicorn` | ASGI server for FastAPI |
| `pydantic` | Request/response validation |
| `streamlit` | Frontend UI framework |
| `pandas` | Excel data loading and manipulation |
| `scikit-learn` | TF-IDF vectorizer and cosine similarity |
| `numpy` | Numerical operations |
| `openpyxl` | Reading `.xlsx` Excel files |
| `nltk` | NLP utilities (imported but supporting role) |

---

## Environment Variables

| Variable | Used By | Default | Purpose |
|---|---|---|---|
| `PORT` | Both | 8000 / 8501 | Auto-set by Cloud Foundry for server binding |
| `PU_CHATBOT_API_URL` | Frontend | Production CF URL | Points frontend to backend API |

---

## Key Observations

- **Strengths:** Clean separation of concerns, professional UI, robust error handling, cloud-ready
- **Limitations:**
  - No authentication or rate limiting on the API
  - Dataset loaded from disk on every request (no caching)
  - TF-IDF matching may be inaccurate for complex or unseen questions
  - No logging configured
  - Production API URL hardcoded as default in frontend
- **Testing:** Jupyter notebook (`test/ats_cb_test.ipynb`) used for ad-hoc dataset and matching tests; no automated test suite

---

## Project Stats

| Metric | Value |
|---|---|
| Total source files | 9 |
| Backend lines of code | 95 |
| Frontend lines of code | 356 |
| API endpoints | 2 |
| Deployment platform | Cloud Foundry (IBM SAP BTP) |
| Memory per app | 512 MB |
| Data storage | File-based (Excel) |
