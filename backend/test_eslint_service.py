from services.eslint_service import analyse_javascript, parse_eslint_output


def test_parse_eslint_output_maps_messages_to_issue_dicts():
    output = '''[
        {
            "messages": [
                {
                    "severity": 2,
                    "message": "Unexpected console statement.",
                    "line": 3,
                    "column": 5,
                    "ruleId": "no-console"
                }
            ]
        }
    ]'''

    result = parse_eslint_output(output)

    assert result == [{
        "type": 2,
        "message": "Unexpected console statement.",
        "line": 3,
        "column": 5,
        "ruleId": "no-console",
    }]


def test_analyse_javascript_runs_eslint_and_returns_results():
    code = """
function greet(name) {
    return missingVariable;
}
"""

    result = analyse_javascript(code)

    assert result["tool"] == "eslint"
    assert isinstance(result["issues"], list)
    assert any(issue.get("ruleId") == "no-undef" for issue in result["issues"])