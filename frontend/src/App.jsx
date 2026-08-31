import { useState } from "react";
import * as api from "./services/api";
import "./App.css";

function App() {

    const [code, setCode] = useState("");
    const [language, setLanguage] = useState("python");
    const [consent, setConsent] = useState(false);
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState("");

    const handleAnalyse = async () => {

        setLoading(true);
        setError("");
        setResults(null);

        try {

            const data = await api.analyseCode(
                code,
                language
            );

            setResults(data);

        } catch (err) {

            setError(err.message);

        } finally {

            setLoading(false);

        }
    };


    return (
        <div className="app">

            <h1>AI-Assisted Code Review Helper</h1>


            {/* Language selection */}

            <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
            >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="java">Java</option>
            </select>


            {/* Code input */}

            <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="Paste your code here..."
            />


            {/* Security warning */}

            <p>
                Do not submit confidential code, API keys,
                passwords or personal information.
            </p>


            {/* Consent */}

            <label>

                <input
                    type="checkbox"
                    checked={consent}
                    onChange={(e) => setConsent(e.target.checked)}
                />

                I confirm that this code does not contain
                confidential or personal information.

            </label>


            {/* Analyse button */}

            <button
                disabled={!consent || loading || !code.trim()}
                onClick={handleAnalyse}
            >

                {loading
                    ? "Analysing..."
                    : "Analyse Code"
                }

            </button>


            {/* Error */}

            {error && (

                <div className="error">

                    <h2>Error</h2>

                    <p>{error}</p>

                </div>

            )}


            {/* Results */}

            {results && (

                <div className="results">

                    <h2>Review Results</h2>


                    {/* Overall score */}

                    {results.score && (

                        <div className="score">

                            <h3>
                                Overall Score
                            </h3>

                            <p>
                                {results.score.overall}/100
                            </p>

                        </div>

                    )}


                    {/* Score breakdown */}

                    {results.score && (

                        <div className="score-breakdown">

                            <h3>
                                Score Breakdown
                            </h3>

                            <p>
                                Readability:
                                {" "}
                                {results.score.readability}/100
                            </p>

                            <p>
                                Maintainability:
                                {" "}
                                {results.score.maintainability}/100
                            </p>

                            <p>
                                Style:
                                {" "}
                                {results.score.style}/100
                            </p>

                            <p>
                                Bugs:
                                {" "}
                                {results.score.bugs}/100
                            </p>

                        </div>

                    )}


                    {/* Static analysis */}

                    <div className="static-results">

                        <h3>
                            Static Analysis
                        </h3>

                        <p>
                            Tool:{" "}
                            {results.static_analysis?.tool}
                        </p>


                        {results.static_analysis?.issues?.length > 0 ? (

                            <ul>

                                {results.static_analysis.issues.map(
                                    (issue, index) => (

                                        <li key={index}>

                                            <strong>
                                                {issue.type}
                                            </strong>

                                            {" - "}

                                            {issue.message}

                                            {issue.line && (

                                                <span>
                                                    {" "}
                                                    (Line {issue.line})
                                                </span>

                                            )}

                                        </li>

                                    )
                                )}

                            </ul>

                        ) : (

                            <p>
                                No static analysis issues found.
                            </p>

                        )}

                    </div>


                    {/* AI analysis */}

                    <div className="ai-results">

                        <h3>
                            AI Analysis
                        </h3>


                        {results.ai_analysis?.error ? (

                            <p className="error">
                                AI analysis unavailable:
                                {" "}
                                {results.ai_analysis.error}
                            </p>

                        ) : results.ai_analysis?.issues?.length > 0 ? (

                            <ul>

                                {results.ai_analysis.issues.map(
                                    (issue, index) => (

                                        <li key={index}>

                                            <strong>
                                                {issue.severity?.toUpperCase()}
                                            </strong>

                                            {" - "}

                                            <strong>
                                                {issue.category}
                                            </strong>

                                            <p>
                                                {issue.message}
                                            </p>

                                            <p>
                                                <strong>
                                                    Suggestion:
                                                </strong>
                                                {" "}
                                                {issue.suggestion}
                                            </p>

                                            {issue.line && (

                                                <p>
                                                    Line: {issue.line}
                                                </p>

                                            )}

                                        </li>

                                    )
                                )}

                            </ul>

                        ) : (

                            <p>
                                No AI issues found.
                            </p>

                        )}

                    </div>

                </div>

            )}

        </div>
    );
}

export default App;