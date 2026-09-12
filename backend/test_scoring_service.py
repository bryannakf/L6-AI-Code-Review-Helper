from app import app
from services.scoring_service import calculate_score


def test_calculate_score_aggregates_static_and_ai_findings():
    score = calculate_score(
        [
            {"type": "error"},
            {"type": "warning"},
            {"type": "convention"},
        ],
        [
            {"severity": "critical"},
            {"severity": "medium"},
            {"severity": "low"},
        ],
    )

    assert score["overall"] == 86
    assert score["bugs"] == 65
    assert score["maintainability"] == 90
    assert score["readability"] == 92
    assert score["style"] == 95


def test_review_route_rejects_missing_or_sensitive_code():
    client = app.test_client()

    response = client.post(
        "/api/review",
        json={"code": "print('hello')", "language": "python"},
    )
    assert response.status_code == 200
    assert response.get_json()["language"] == "python"

    secret_response = client.post(
        "/api/review",
        json={"code": "password = 'super-secret'\nprint(password)", "language": "python"},
    )
    assert secret_response.status_code == 400
    assert "Potential secret" in secret_response.get_json()["error"]


def test_review_route_validates_request_shape():
    client = app.test_client()

    response = client.post("/api/review", json={})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Code is required"