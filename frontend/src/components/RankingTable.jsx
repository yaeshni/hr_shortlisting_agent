function medalColor(index) {
  if (index === 0) return "#F5C518"
  if (index === 1) return "#A8A9AD"
  if (index === 2) return "#cd7f32"
  return "var(--text-muted)"
}

function scoreColor(score) {
  if (score >= 7.5) return "#22c55e"
  if (score >= 5) return "#f59e0b"
  return "#ef4444"
}

function RankingTable({ results }) {
  return (
    <div className="table-card">
      <table className="rank-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Candidate</th>
            <th>Similarity</th>
            <th>Total Score</th>
          </tr>
        </thead>
        <tbody>
          {results.map((candidate, index) => (
            <tr key={index} className={index === 0 ? "top-row" : ""}>
              <td>
                <span
                  className="rank-badge"
                  style={{ color: medalColor(index) }}
                >
                  #{index + 1}
                </span>
              </td>
              <td className="candidate-name">{candidate.candidate}</td>
              <td>
                <div className="score-bar-wrap">
                  <div
                    className="score-bar"
                    style={{ width: `${candidate.similarity_score}%` }}
                  />
                  <span className="score-label">{candidate.similarity_score}%</span>
                </div>
              </td>
              <td>
                <span
                  className="total-score"
                  style={{ color: scoreColor(candidate.evaluation.total_score) }}
                >
                  {candidate.evaluation.total_score} / 10
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default RankingTable
