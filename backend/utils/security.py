import re


SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9_-]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"(?i)(password|passwd|pwd)\s*=\s*[\"'][^\"']+[\"']",
    r"(?i)(api_key|apikey|secret|token)\s*=\s*[\"'][^\"']+[\"']",
]


def detect_secrets(code):

    findings = []

    for pattern in SECRET_PATTERNS:
        matches = re.finditer(pattern, code)

        for match in matches:
            line = code[:match.start()].count("\n") + 1

            findings.append({
                "type": "security",
                "message": "Possible hardcoded secret detected.",
                "line": line
            })

    return findings