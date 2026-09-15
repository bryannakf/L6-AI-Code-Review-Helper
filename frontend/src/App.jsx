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

  const [securityConfirmationRequired, setSecurityConfirmationRequired] =
    useState(false);


  const clearForm = () => {
    setCode("");
    setConsent(false);
    setResults(null);
    setError("");
    setSecurityError("");
    setSecurityConfirmationRequired(false);
  };


  const handleAnalyse = async (secretConfirmed = false) => {
    setLoading(true);

    setError("");
    setSecurityError("");

    // Only clear existing results when starting a new analysis.
    // If the user is confirming a possible false positive,
    // keep the current page state until the new analysis completes.
    if (!secretConfirmed) {
      setResults(null);
    }

    try {
      const start = performance.now();

      const data = await api.analyseCode(
        code,
        language,
        secretConfirmed
      );

      const end = performance.now();

      const analysisTime = (end - start) / 1000;

      console.log(
        "Analysis took " +
          analysisTime.toFixed(2) +
          " seconds"
      );


      // A possible secret was detected.
      // Ask the user to confirm before continuing.
      if (
        data.security &&
        data.security.confirmation_required
      ) {
        setSecurityConfirmationRequired(true);

        return;
      }


      // Analysis completed successfully.
      setSecurityConfirmationRequired(false);

      setResults(data);

    } catch (err) {

      if (
        err.response &&
        err.response.data &&
        err.response.data.security
      ) {
        setSecurityConfirmationRequired(true);

        setSecurityError(
          err.response.data.error ||
            "Potential sensitive information detected."
        );

      } else {
        setError(
          err.message ||
            "An unexpected error occurred."
        );
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

      securityConfirmationRequired={
        securityConfirmationRequired
      }

      handleAnalyse={handleAnalyse}

      clearForm={clearForm}
    />
  );
}


export default App;