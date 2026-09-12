import json
from types import SimpleNamespace

import services.ai_service as ai_service


class FakeCompletions:
    def __init__(self, payload):
        self.payload = payload

    def create(self, **kwargs):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content=self.payload)
                )
            ]
        )


def test_analyse_code_returns_openai_issues(monkeypatch):
    payload = json.dumps({
        "issues": [{
            "severity": "high",
            "category": "bugs",
            "message": "Potential divide-by-zero risk",
            "suggestion": "Guard against zero values",
            "line": 3,
        }]
    })

    monkeypatch.setattr(
        ai_service,
        "client",
        SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions(payload))),
    )

    result = ai_service.analyse_code("def divide(a, b):\n    return a / b\n", "python")

    assert result["tool"] == "openai"
    assert result["issues"][0]["severity"] == "high"
    assert result["issues"][0]["line"] == 3


def test_analyse_code_handles_invalid_json(monkeypatch):
    monkeypatch.setattr(
        ai_service,
        "client",
        SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions("not-json"))),
    )

    result = ai_service.analyse_code("print('hello')\n", "python")

    assert result["tool"] == "openai"
    assert result["issues"] == []
    assert result["error"] == "AI returned invalid JSON"