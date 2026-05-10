# 🤖 HR Resume Shortlisting Agent

An AI-powered full-stack web app that automatically evaluates and ranks candidate resumes against a job description — using LLMs, semantic embeddings, and skill matching.

---

## ✨ Features

- 📄 Upload a Job Description (PDF, DOCX, or TXT)
- 👥 Upload multiple candidate resumes at once
- 🧠 LLM-powered structured data extraction via OpenRouter (GPT-3.5)
- 📐 Semantic similarity scoring using SentenceTransformers
- 🏆 Candidates ranked by a weighted score across 5 dimensions
- 📊 Visual score breakdown with matched skills highlighted
- 📑 PDF report generation for shortlisted candidates

---

## 🛠️ Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — REST API framework
- [SentenceTransformers](https://www.sbert.net/) — semantic embeddings (`all-MiniLM-L6-v2`)
- [OpenRouter](https://openrouter.ai/) — LLM API (GPT-3.5-turbo)
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF text extraction
- [ReportLab](https://www.reportlab.com/) — PDF report generation

**Frontend**
- [React](https://react.dev/) + [Vite](https://vitejs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Axios](https://axios-http.com/)

---

## 📁 Project Structure

```
Resume_shortlisting_Agent/
├── backend/
│   ├── services/
│   │   ├── embeddings.py        # Semantic similarity via SentenceTransformers
│   │   ├── llm_extractor.py     # LLM-based structured data extraction
│   │   ├── override_manager.py  # Manual override persistence
│   │   ├── parser.py            # PDF / DOCX / TXT text extraction
│   │   ├── report_generator.py  # PDF report generation
│   │   └── scorer.py            # Weighted candidate scoring logic
│   ├── reports/                 # Generated PDF reports saved here
│   ├── app.py                   # FastAPI app + API routes
│   ├── requirements.txt
│   └── .env                     # API keys (not committed)
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── CandidateCard.jsx
    │   │   ├── RankingTable.jsx
    │   │   └── UploadForm.jsx
    │   ├── App.jsx
    │   ├── App.css
    │   ├── index.css
    │   └── main.jsx
    ├── index.html
    └── package.json
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- An [OpenRouter](https://openrouter.ai/) API key

---

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Backend setup

```bash
cd backend
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows (Git Bash)
source venv/Scripts/activate

pip install -r requirements.txt
```

Create a `.env` file inside the `backend/` folder:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Start the backend:

```bash
uvicorn app:app --reload
```

Backend runs at → `http://127.0.0.1:8000`

---

### 3. Frontend setup

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at → `http://localhost:5173`

---

## 🚀 Usage

1. Open `http://localhost:5173` in your browser
2. Upload a **Job Description** file (PDF, DOCX, or TXT)
3. Upload one or more **candidate resumes**
4. Click **Evaluate Candidates**
5. View ranked results with score breakdowns and matched skills

---

## 📊 Scoring Breakdown

Each candidate is scored across 5 dimensions:

| Dimension | Weight | How it's calculated |
|---|---|---|
| Skills Match | 30% | Required skills matched from JD |
| Experience | 25% | Number of experience entries found |
| Education | 15% | Number of education entries found |
| Projects | 20% | Number of projects found |
| Communication | 10% | Certifications found |

---

## 🔒 Environment Variables

| Variable | Description |
|---|---|
| `OPENROUTER_API_KEY` | Your OpenRouter API key |

Never commit your `.env` file. It is already listed in `.gitignore`.

---

## 📝 License

MIT License — feel free to use, modify, and distribute.
