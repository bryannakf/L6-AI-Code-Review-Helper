export function getScoreLabel(score) {
  if (score >= 90) return "Excellent";
  if (score >= 75) return "Good";
  if (score >= 50) return "Fair";
  return "Needs Improvement";
}

export function getSeverityClass(severity) {
  const normalized = String(severity || "info").toLowerCase();

  if (normalized.includes("critical") || normalized.includes("error")) {
    return "critical";
  }

  if (normalized.includes("warning") || normalized.includes("medium")) {
    return "medium";
  }

  return "low";
}
