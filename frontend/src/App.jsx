import { useState } from "react"
import axios from "axios"
import UploadForm from "./components/UploadForm"
import CandidateCard from "./components/CandidateCard"
import RankingTable from "./components/RankingTable"

function App() {
  const [jd, setJd] = useState(null)
  const [resumes, setResumes] = useState([])
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async () => {
    if (!jd || resumes.length === 0) {
      setError("Please upload a Job Description and at least one resume.")
      return
    }
    setLoading(true)
    setError("")
    setResults([])

    const formData = new FormData()
    formData.append("jd", jd)
    Array.from(resumes).forEach((file) => formData.append("resumes", file))

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/evaluate-multiple/",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      )
      setResults(response.data.ranked_candidates)
    } catch (err) {
      const detail = err?.response?.data?.detail
      setError(
        detail
          ? `Backend error: ${detail}`
          : "Could not connect to backend. Make sure it is running on port 8000."
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <div className="noise-overlay" />

      <header className="hero-header">
        <div className="header-badge">AI-Powered · HR Tool</div>
        <h1 className="hero-title">
          Resume <span className="accent-text">Shortlisting</span> Agent
        </h1>
        <p className="hero-sub">
          Upload a job description and candidate resumes — get ranked results in seconds.
        </p>
      </header>

      <main className="main-content">
        <UploadForm
          setJd={setJd}
          setResumes={setResumes}
          handleSubmit={handleSubmit}
          loading={loading}
          jd={jd}
          resumes={resumes}
        />

        {error && (
          <div className="error-bar">
            <span className="error-icon">⚠</span> {error}
          </div>
        )}

        {loading && (
          <div className="loading-state">
            <div className="spinner" />
            <p className="loading-text">Analysing candidates…</p>
          </div>
        )}

        {results.length > 0 && (
          <div className="results-section">
            <div className="results-header">
              <h2 className="results-title">
                {results.length} Candidate{results.length > 1 ? "s" : ""} Ranked
              </h2>
              <span className="results-pill">Sorted by score</span>
            </div>
            <RankingTable results={results} />
            <div className="cards-grid">
              {results.map((candidate, index) => (
                <CandidateCard key={index} candidate={candidate} index={index} />
              ))}
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        Built with FastAPI · SentenceTransformers · OpenRouter
      </footer>
    </div>
  )
}

export default App
