import test from "node:test";
import assert from "node:assert/strict";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";

import { getScoreLabel, getSeverityClass } from "./src/utils/review.js";
import AppContent from "./src/AppContent.jsx";

const renderApp = (props = {}) =>
  renderToStaticMarkup(
    React.createElement(AppContent, {
      code: "",
      setCode: () => {},
      language: "python",
      setLanguage: () => {},
      consent: false,
      setConsent: () => {},
      loading: false,
      results: null,
      error: "",
      securityError: "",
      handleAnalyse: () => {},
      clearForm: () => {},
      ...props,
    }),
  );

test("getScoreLabel returns the correct status for a score", () => {
  assert.equal(getScoreLabel(95), "Excellent");
  assert.equal(getScoreLabel(78), "Good");
  assert.equal(getScoreLabel(60), "Fair");
  assert.equal(getScoreLabel(35), "Needs Improvement");
});

test("getSeverityClass maps issue severities to CSS classes", () => {
  assert.equal(getSeverityClass("critical"), "critical");
  assert.equal(getSeverityClass("warning"), "medium");
  assert.equal(getSeverityClass("info"), "low");
  assert.equal(getSeverityClass("ERROR"), "critical");
});

test("app renders all main form elements and static text", () => {
  const html = renderApp();

  assert.match(html, /AI Code Review Helper/);
  assert.match(html, /Submit a code snippet/);
  assert.match(html, /Programming language/);
  assert.match(html, /Code snippet/);
  assert.match(html, /Security reminder/);
  assert.match(html, /Analyse Code/);
  assert.match(html, /Clear/);
  assert.match(html, /Use this tool for non-sensitive code only/);
});

test("app shows error and security notification states", () => {
  const html = renderApp({
    code: "print('hello')",
    consent: true,
    error: "Backend unavailable",
    securityError: "Sensitive code detected",
  });

  assert.match(html, /Backend unavailable/);
  assert.match(html, /Sensitive code detected/);
});

test("app renders analysis results with score, static issues, and AI issues", () => {
  const html = renderApp({
    code: "def demo():\n    value = 1\n    return value",
    consent: true,
    results: {
      analysis_time: 1.23,
      score: {
        overall: 88,
        readability: 90,
        maintainability: 85,
        style: 92,
        bugs: 84,
      },
      static_analysis: {
        tool: "pylint",
        issues: [{ type: "warning", message: "Unused variable", line: 2 }],
      },
      ai_analysis: {
        issues: [
          {
            severity: "medium",
            category: "maintainability",
            message: "Refactor this function",
            suggestion: "Extract helper",
            line: 1,
          },
        ],
      },
    },
  });

  assert.match(html, /Review Results/);
  assert.match(html, /Overall Quality Score/);
  assert.match(html, /Good/);
  assert.match(html, /Readability/);
  assert.match(html, /Maintainability/);
  assert.match(html, /Static Analysis/);
  assert.match(html, /AI Analysis/);
  assert.match(html, /Unused variable/);
  assert.match(html, /Refactor this function/);
});

test("app renders no-issues messages when results are empty", () => {
  const html = renderApp({
    results: {
      static_analysis: { tool: "pylint", issues: [] },
      ai_analysis: { issues: [] },
      score: {
        overall: 95,
        readability: 95,
        maintainability: 95,
        style: 95,
        bugs: 95,
      },
    },
  });

  assert.match(html, /No static analysis issues found\./);
  assert.match(html, /No AI issues found\./);
});
