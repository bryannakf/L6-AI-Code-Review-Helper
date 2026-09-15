from backend.utils.security import detect_secrets


def test_detect_secrets_returns_empty_for_safe_code():
    code = """
def add(a, b):
    return a + b
"""

    findings = detect_secrets(code)

    assert findings == []


def test_detect_secrets_detects_openai_style_key():
    code = "api_key = 'sk-abcdefghijklmnopqrstuvwxyz1234'"

    findings = detect_secrets(code)

    assert len(findings) >= 1
    assert all(item["type"] == "security" for item in findings)
    assert all(item["line"] == 1 for item in findings)


def test_detect_secrets_detects_aws_access_key():
    code = "aws_key = 'AKIA1234567890ABCDEF'"

    findings = detect_secrets(code)

    assert len(findings) == 1
    assert findings[0]["type"] == "security"
    assert findings[0]["line"] == 1


def test_detect_secrets_detects_password_assignment_case_insensitive():
    code = """
def connect():
    Password = \"super-secret\"
    return True
"""

    findings = detect_secrets(code)

    assert len(findings) == 1
    assert findings[0]["line"] == 3


def test_detect_secrets_detects_token_assignment_and_reports_line():
    code = """
name = \"demo\"
token = \"abc123\"
print(name)
"""

    findings = detect_secrets(code)

    assert len(findings) == 1
    assert findings[0]["line"] == 3
