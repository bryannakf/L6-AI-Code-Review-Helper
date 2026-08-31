import { useState } from "react";
import * as api from "./services/api";
import "./App.css";

const getScoreLabel = (score) => {
  if (score >= 85) return "Excellent";
  if (score >= 70) return "Good";
  if (score >= 50) return "Fair";
  return "Needs Improvement";
};

const getSeverityClass = (severity = "") => {
  const value = String(severity).toLowerCase();
  if (["critical", "high", "error"].includes(value)) return "critical";
  if (["medium", "warning"].includes(value)) return "medium";
  return "low";
};

function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [consent, setConsent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");

  const clearForm = () => {
    setCode("");
    setConsent(false);
    setResults(null);
    setError("");
  };

  const handleAnalyse = async () => {
    setLoading(true);
    setError("");
    setResults(null);

    try {
      // Start frontend timer
      const start = performance.now();

      // Send code to backend
      const data = await api.analyseCode(code, language);

      // Stop frontend timer
      const end = performance.now();

      const analysisTime = (end - start) / 1000;

      console.log("Analysis took " + analysisTime.toFixed(2) + " seconds");

      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="brand">
            <div className="brand-icon">AI</div>
            <div>
              <h1>Code Review Helper</h1>
              <p>Fast quality checks with clear, practical feedback</p>
            </div>
          </div>

          <div className="status">
            <span className="status-dot" />
            <span>Ready to analyse</span>
          </div>
        </div>
      </header>

      <main className="main-content">
        <section className="intro">
          <p className="eyebrow">SECURE REVIEW FLOW</p>
          <h2>Review code quality before you ship</h2>
          <p>
            Submit a snippet, run static and AI checks, and get a clear quality
            score with actionable suggestions.
          </p>
        </section>

        <section className="review-card">
          <div className="editor-section">
            <div className="editor-header">
              <label htmlFor="language-select">Programming language</label>
              <select
                id="language-select"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="java">Java</option>
              </select>
            </div>

            <label htmlFor="code-editor">Code snippet</label>
            <textarea
              id="code-editor"
              className="code-editor"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Paste your code here..."
            />
            <p className="character-count">{code.length} characters</p>

            <div className="consent-container">
              <div className="security-warning">
                <div className="warning-icon">!</div>
                <div>
                  <h3>Security reminder</h3>
                  <p>
                    Do not submit confidential code, API keys, passwords, or
                    personal information.
                  </p>
                </div>
              </div>

              <label className="consent-checkbox">
                <input
                  type="checkbox"
                  checked={consent}
                  onChange={(e) => setConsent(e.target.checked)}
                />
                <span>
                  I confirm that this code does not contain confidential or
                  personal information.
                </span>
              </label>
            </div>

            <div className="action-buttons">
              <button
                className="primary-button"
                disabled={!consent || loading || !code.trim()}
                onClick={handleAnalyse}
              >
                {loading && <span className="spinner" />}
                {loading ? "Analysing..." : "Analyse Code"}
              </button>

              <button
                className="secondary-button"
                disabled={loading && !code}
                onClick={clearForm}
              >
                Clear
              </button>
            </div>

            {error && (
              <div className="error-message">
                <strong>Request failed</strong>
                <p>{error}</p>
              </div>
            )}
          </div>
        </section>

        <section className="how-it-works">
          <h2>How it works</h2>
          <div className="steps">
            <div className="step">
              <p className="step-number">STEP 1</p>
              <h3>Paste snippet</h3>
              <p>Add the code you want reviewed.</p>
            </div>
            <div className="step">
              <p className="step-number">STEP 2</p>
              <h3>Confirm safety</h3>
              <p>Verify there is no sensitive information.</p>
            </div>
            <div className="step">
              <p className="step-number">STEP 3</p>
              <h3>Run analysis</h3>
              <p>Static checks and AI feedback are generated.</p>
            </div>
            <div className="step">
              <p className="step-number">STEP 4</p>
              <h3>Take action</h3>
              <p>Use prioritized suggestions to improve quality.</p>
            </div>
          </div>
        </section>

        {results && (
          <section className="results-container">
            <div className="results-header">
              <div>
                <p className="results-label">ANALYSIS COMPLETE</p>
                <h2>Review Results</h2>
              </div>

              {results.analysis_time !== undefined && (
                <div className="analysis-time">
                  <span>Total analysis time</span>
                  <strong>{results.analysis_time} seconds</strong>
                </div>
              )}
            </div>

            {results.score && (
              <>
                <div className="score-card">
                  <div className="score-circle">
                    <span className="score-number">
                      {results.score.overall}
                    </span>
                    <span className="score-total">/100</span>
                  </div>

                  <div className="score-information">
                    <h2>Overall Quality Score</h2>
                    <p>
                      Current quality status:{" "}
                      <span className="score-label">
                        {getScoreLabel(results.score.overall)}
                      </span>
                    </p>
                  </div>
                </div>

                <div className="score-breakdown">
                  {[
                    ["Readability", results.score.readability],
                    ["Maintainability", results.score.maintainability],
                    ["Style", results.score.style],
                    ["Bugs", results.score.bugs],
                  ].map(([label, value]) => (
                    <div className="score-metric" key={label}>
                      <span>{label}</span>
                      <strong>{value}</strong>
                      <div className="progress-bar">
                        <div
                          className="progress-value"
                          style={{
                            width: `${Math.max(0, Math.min(100, value || 0))}%`,
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}

            {results.ai_analysis?.summary && (
              <div className="summary">
                <h3>AI Summary</h3>
                <p>{results.ai_analysis.summary}</p>
              </div>
            )}

            <div className="issue-section">
              <h3>Static Analysis</h3>
              <p className="tool">
                Tool: {results.static_analysis?.tool || "N/A"}
              </p>

              {results.static_analysis?.issues?.length > 0 ? (
                results.static_analysis.issues.map((issue, index) => (
                  <div className="issue" key={`static-${index}`}>
                    <div className="issue-header">
                      <span
                        className={`severity ${getSeverityClass(issue.type)}`}
                      >
                        {issue.type || "info"}
                      </span>
                      {issue.line && (
                        <span className="line">Line {issue.line}</span>
                      )}
                    </div>
                    <p className="issue-message">{issue.message}</p>
                  </div>
                ))
              ) : (
                <p className="no-issues">No static analysis issues found.</p>
              )}
            </div>

            <div className="issue-section">
              <h3>AI Analysis</h3>

              {results.ai_analysis?.error ? (
                <div className="error-message">
                  <strong>AI analysis unavailable</strong>
                  <p>{results.ai_analysis.error}</p>
                </div>
              ) : results.ai_analysis?.issues?.length > 0 ? (
                results.ai_analysis.issues.map((issue, index) => (
                  <div className="issue" key={`ai-${index}`}>
                    <div className="issue-header">
                      <span
                        className={`severity ${getSeverityClass(issue.severity)}`}
                      >
                        {issue.severity || "info"}
                      </span>
                      <span className="tool">
                        {issue.category || "General"}
                      </span>
                      {issue.line && (
                        <span className="line">Line {issue.line}</span>
                      )}
                    </div>
                    <p className="issue-message">{issue.message}</p>
                    {issue.suggestion && <p>{issue.suggestion}</p>}
                  </div>
                ))
              ) : (
                <p className="no-issues">No AI issues found.</p>
              )}
            </div>

            <div className="ai-disclaimer">
              AI suggestions are advisory and should be reviewed with project
              context before applying.
            </div>
          </section>
        )}
      </main>

      <footer>
        <p>AI-Assisted Code Review Helper</p>
        <p>Use this tool for non-sensitive code only</p>
      </footer>
    </div>
  );
}

export default App;
