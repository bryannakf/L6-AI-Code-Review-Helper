import json
from types import SimpleNamespace

import services.ai_service as ai_service


class FakeCompletions:
    def __init__(self, payload):
        self.payloads = payload if isinstance(payload, list) else [payload]
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        payload = self.payloads[min(len(self.calls) - 1, len(self.payloads) - 1)]
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content=payload)
                )
            ]
        )


def test_analyse_code_returns_openai_issues(monkeypatch):
    initial_payload = json.dumps({
        "issues": [{
            "severity": "high",
            "category": "bugs",
            "message": "Potential divide-by-zero risk",
            "suggestion": "Guard against zero values",
            "line": 3,
        }],
        "summary": "Initial findings"
    })
    remediation_payload = json.dumps({
        "summary": "Add a zero guard before dividing.",
        "actions": [{
            "line": 3,
            "category": "bugs",
            "issue": "Potential divide-by-zero risk",
            "action": "Check the denominator before dividing.",
            "suggested_code": "if b == 0:\n    return 0",
            "reason": "This prevents a runtime ZeroDivisionError."
        }]
    })

    fake_completions = FakeCompletions([initial_payload, remediation_payload])

    monkeypatch.setattr(
        ai_service,
        "client",
        SimpleNamespace(chat=SimpleNamespace(completions=fake_completions)),
    )

    result = ai_service.analyse_code(
        "def divide(a, b):\n    return a / b\n",
        "python",
        [{"line": 2, "message": "Possible divide-by-zero"}]
    )

    assert result["tool"] == "openai"
    assert result["issues"][0]["severity"] == "high"
    assert result["issues"][0]["line"] == 3
    assert result["summary"] == "Add a zero guard before dividing."
    assert result["actions"][0]["line"] == 3
    assert "STATIC ANALYSIS FINDINGS" in fake_completions.calls[1]["messages"][0]["content"]


def test_analyse_code_handles_invalid_json(monkeypatch):
    monkeypatch.setattr(
        ai_service,
        "client",
        SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions("not-json"))),
    )

    result = ai_service.analyse_code("print('hello')\n", "python", [])

    assert result["tool"] == "openai"
    assert result["issues"] == []
    assert result["error"] == "AI returned invalid JSON"