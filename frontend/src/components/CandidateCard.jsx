function ScoreRow({ label, data }) {
  const pct = (data.score / 10) * 100
  return (
    <div className="score-row">
      <div className="score-row-header">
        <span className="score-row-label">{label}</span>
        <span className="score-row-value">{data.score}/10</span>
      </div>
      <div className="score-track">
        <div
          className="score-fill"
          style={{ width: `${pct}%`, opacity: 0.7 + pct / 300 }}
        />
      </div>
      <p className="score-reason">{data.reason}</p>
    </div>
  )
}

function CandidateCard({ candidate, index }) {
  const ev = candidate.evaluation
  const isTop = index === 0

  return (
    <div className={`candidate-card ${isTop ? "top-candidate" : ""}`}>
      {isTop && <div className="top-ribbon">Top Pick</div>}

      <div className="card-header">
        <div className="rank-circle">#{index + 1}</div>
        <div>
          <h2 className="card-name">{candidate.candidate}</h2>
          <p className="card-meta">
            Similarity&nbsp;
            <strong>{candidate.similarity_score}%</strong>
            &nbsp;·&nbsp;Total Score&nbsp;
            <strong>{ev.total_score}/10</strong>
          </p>
        </div>
      </div>

      <div className="score-breakdown">
        <ScoreRow label="Skills Match"         data={ev.skills_match} />
        <ScoreRow label="Experience"           data={ev.experience_relevance} />
        <ScoreRow label="Education"            data={ev.education} />
        <ScoreRow label="Projects"             data={ev.projects} />
        <ScoreRow label="Communication"        data={ev.communication} />
      </div>

      {ev.skills_match?.matched_required?.length > 0 && (
        <div className="matched-skills">
          <p className="skills-title">Matched Skills</p>
          <div className="skills-list">
            {ev.skills_match.matched_required.map((s, i) => (
              <span key={i} className="skill-tag">{s}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default CandidateCard
