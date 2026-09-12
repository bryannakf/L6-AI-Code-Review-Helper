import { useState } from "react";
import * as api from "./services/api";
import AppContent from "./AppContent.jsx";
import "./App.css";

function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [consent, setConsent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");
  const [securityError, setSecurityError] = useState("");

  const clearForm = () => {
    setCode("");
    setConsent(false);
    setResults(null);
    setError("");
    setSecurityError("");
  };

  const handleAnalyse = async () => {
    setLoading(true);
    setError("");
    setSecurityError("");
    setResults(null);

    try {
      const start = performance.now();
      const data = await api.analyseCode(code, language);
      const end = performance.now();
      const analysisTime = (end - start) / 1000;

      console.log("Analysis took " + analysisTime.toFixed(2) + " seconds");

      setResults(data);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.security) {
        setSecurityError(err.response.data.error);
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppContent
      code={code}
      setCode={setCode}
      language={language}
      setLanguage={setLanguage}
      consent={consent}
      setConsent={setConsent}
      loading={loading}
      results={results}
      error={error}
      securityError={securityError}
      handleAnalyse={handleAnalyse}
      clearForm={clearForm}
    />
  );
}

export default App;
