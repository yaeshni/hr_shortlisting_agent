import { useRef } from "react"

function UploadForm({ setJd, setResumes, handleSubmit, loading, jd, resumes }) {
  const jdRef = useRef()
  const resumesRef = useRef()

  return (
    <div className="upload-card">
      <div className="upload-grid">

        <div className="upload-zone">
          <div className="upload-icon">📄</div>
          <p className="upload-label">Job Description</p>
          <p className="upload-hint">PDF, DOCX, or TXT</p>
          <input
            ref={jdRef}
            type="file"
            accept=".pdf,.docx,.txt"
            style={{ display: "none" }}
            onChange={(e) => setJd(e.target.files[0])}
          />
          <button
            className="upload-btn"
            onClick={() => jdRef.current.click()}
          >
            {jd ? `✓ ${jd.name}` : "Choose File"}
          </button>
        </div>

        <div className="upload-divider" />

        <div className="upload-zone">
          <div className="upload-icon">👥</div>
          <p className="upload-label">Candidate Resumes</p>
          <p className="upload-hint">Multiple files supported</p>
          <input
            ref={resumesRef}
            type="file"
            accept=".pdf,.docx,.txt"
            multiple
            style={{ display: "none" }}
            onChange={(e) => setResumes(e.target.files)}
          />
          <button
            className="upload-btn"
            onClick={() => resumesRef.current.click()}
          >
            {resumes && resumes.length > 0
              ? `✓ ${resumes.length} file${resumes.length > 1 ? "s" : ""} selected`
              : "Choose Files"}
          </button>
        </div>
      </div>

      <button
        className={`evaluate-btn ${loading ? "loading" : ""}`}
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Evaluating…" : "Evaluate Candidates →"}
      </button>
    </div>
  )
}

export default UploadForm