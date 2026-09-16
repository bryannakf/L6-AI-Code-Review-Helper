import React from "react";
import { getScoreLabel, getSeverityClass } from "./utils/review";

void React;

function AppContent({
  code,
  setCode,

  language,
  setLanguage,

  consent,
  setConsent,

  loading,

  results,

  error,

  securityError,

  securityConfirmationRequired,

  handleAnalyse,

  clearForm,
}) {
  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="brand">
            <div>
              <h1>AI Code Review Helper</h1>
            </div>
          </div>

          <div className="status">
            {securityError && (
              <div className="security-error">{securityError}</div>
            )}
          </div>
        </div>
      </header>

      <main className="main-content">
        <section className="intro">
          <h2>Submit a code snippet</h2>

          <p>
            Static and AI checks with a clear quality score with actionable
            suggestions.
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

                <option value="csharp">C#</option>
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

            {/* 
              Confirmation shown when the secret detector
              identifies a pattern that may be a secret.
            */}

            {securityConfirmationRequired && (
              <div className="security-confirmation">
                <div className="warning-icon">!</div>

                <div className="security-confirmation-content">
                  <h4>Potential sensitive information detected</h4>

                  <p>
                    A pattern resembling a secret or credential was detected in
                    your code. Please check your code and make sure it does not
                    contain API keys, passwords, tokens, confidential
                    information or personal data.
                  </p>

                  <p>
                    If you have checked the code and confirm that the detected
                    pattern is not sensitive information, you can continue.
                  </p>

                  <div className="confirmation-buttons">
                    <button
                      className="primary-button"
                      onClick={() => handleAnalyse(true)}
                      disabled={loading}
                    >
                      {loading && <span className="spinner" />}

                      {loading
                        ? "Continuing..."
                        : "I confirm there is no sensitive information"}
                    </button>

                    <button
                      className="secondary-button"
                      onClick={() => clearForm()}
                      disabled={loading}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            )}

            <div className="action-buttons">
              <button
                className="primary-button"
                disabled={
                  !consent ||
                  loading ||
                  !code.trim() ||
                  securityConfirmationRequired
                }
                onClick={() => handleAnalyse(false)}
              >
                {loading && <span className="spinner" />}

                {loading ? "Analysing..." : "Analyse Code"}
              </button>

              <button
                className="secondary-button"
                disabled={loading}
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

            {results.ai_analysis?.actions?.length > 0 && (
              <div className="actions-section">
                <h3>Recommended Actions</h3>

                <div className="actions-list">
                  {results.ai_analysis.actions.map((action, index) => (
                    <div className="issue" key={`action-${index}`}>
                      <div className="issue-header">
                        <span
                          className={`severity ${getSeverityClass(
                            action.severity || action.category,
                          )}`}
                        >
                          {action.category || "action"}
                        </span>

                        {action.line && (
                          <span className="line">Line {action.line}</span>
                        )}
                      </div>

                      <p className="issue-message">{action.issue}</p>

                      {action.action && <p>{action.action}</p>}

                      {action.reason && <p>{action.reason}</p>}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <details className="issue-section issue-accordion">
              <summary className="issue-accordion-summary">
                <div>
                  <p className="issue-accordion-label">STATIC ANALYSIS</p>

                  <h3>Static Analysis</h3>
                </div>

                <div className="issue-accordion-meta">
                  <span>
                    {results.static_analysis?.issues?.length || 0} finding
                    {(results.static_analysis?.issues?.length || 0) === 1
                      ? ""
                      : "s"}
                  </span>

                  <span className="issue-accordion-caret" aria-hidden="true">
                    ▾
                  </span>
                </div>
              </summary>

              <div className="issue-accordion-body">
                <p className="tool">
                  Tool: {results.static_analysis?.tool || "N/A"}
                </p>

                {results.static_analysis?.issues?.length > 0 ? (
                  results.static_analysis.issues.map((issue, index) => (
                    <div className="issue" key={`static-${index}`}>
                      <div className="issue-header">
                        <span
                          className={`severity ${getSeverityClass(
                            issue.severity || issue.type,
                          )}`}
                        >
                          {issue.severity || issue.type || "info"}
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
            </details>

            <details className="issue-section issue-accordion">
              <summary className="issue-accordion-summary">
                <div>
                  <p className="issue-accordion-label">AI ANALYSIS</p>

                  <h3>AI Analysis</h3>
                </div>

                <div className="issue-accordion-meta">
                  <span>
                    {results.ai_analysis?.error
                      ? "Unavailable"
                      : `${results.ai_analysis?.issues?.length || 0} finding${
                          (results.ai_analysis?.issues?.length || 0) === 1
                            ? ""
                            : "s"
                        }`}
                  </span>

                  <span className="issue-accordion-caret" aria-hidden="true">
                    ▾
                  </span>
                </div>
              </summary>

              <div className="issue-accordion-body">
                {results.ai_analysis?.error ? (
                  <div className="error-message">
                    <strong>AI analysis unavailable</strong>

                    <p>{results.ai_analysis.error}</p>
                  </div>
                ) : (
                  <>
                    <div className="issue-section-inner">
                      <h4>AI Findings</h4>

                      {results.ai_analysis?.issues?.length > 0 ? (
                        results.ai_analysis.issues.map((issue, index) => (
                          <div className="issue" key={`ai-${index}`}>
                            <div className="issue-header">
                              <span
                                className={`severity ${getSeverityClass(
                                  issue.severity,
                                )}`}
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
                        <p className="no-issues">No AI findings identified.</p>
                      )}
                    </div>
                  </>
                )}
              </div>
            </details>

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

export default AppContent;
