from services.pylint_service import analyse_python, parse_pylint_output


def test_parse_pylint_output_returns_issue_records():
    payload = '''[
        {
            "type": "warning",
            "message": "Missing function docstring",
            "line": 1,
            "column": 0,
            "symbol": "missing-function-docstring"
        }
    ]'''

    result = parse_pylint_output(payload)

    assert result == [{
        "type": "warning",
        "message": "Missing function docstring",
        "line": 1,
        "column": 0,
        "symbol": "missing-function-docstring",
    }]


def test_analyse_python_runs_pylint_and_reports_issues():
    code = """
def add(a, b):
    return a + b
"""

    result = analyse_python(code)

    assert result["tool"] == "pylint"
    assert isinstance(result["issues"], list)
    assert any(issue.get("symbol") == "missing-function-docstring" for issue in result["issues"])