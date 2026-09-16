import json
import os

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env
load_dotenv()


# Create OpenAI client only when credentials are available.
# In CI and local development without a configured API key, the backend should
# fail gracefully instead of crashing at import time.
client = None
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)


def _call_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def _load_json_response(response_text):
    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        return None


def analyse_code(code, language, static_issues=None):
    """
    Analyse submitted code using OpenAI.

    Returns structured AI findings and remediation actions.
    """

    static_issues = static_issues or []

    initial_prompt = f"""
    You are an experienced software code reviewer.

    Review the following {language} code.

    Identify genuine issues relating to:

    - Bugs
    - Security
    - Maintainability
    - Readability
    - Code quality
    - Poor coding practices

    Do not invent problems. Only report issues that are reasonably supported
    by the code.

    For every issue, provide:

    - severity: critical, high, medium, or low
    - category: bugs, security, maintainability, readability, or style
    - message: a clear explanation of the problem
    - suggestion: a practical improvement
    - line: the approximate line number where the issue occurs

    Return ONLY valid JSON using this structure:

    {{
        "summary": "Brief overall assessment",
        "issues": [
            {{
                "severity": "high",
                "category": "bugs",
                "message": "Description of the issue",
                "suggestion": "How the issue could be improved",
                "line": 1
            }}
        ]
    }}

    If there are no issues, return:

    {{
        "summary": "No significant issues were found.",
        "issues": []
    }}

    Code to review:

    ```{language}
    {code}
    """

    remediation_prompt = f"""
    You are an experienced software developer performing a code review.

    Your task is to turn review findings into actionable remediation guidance.

    ORIGINAL CODE:
    {code}

    STATIC ANALYSIS FINDINGS:
    {json.dumps(static_issues, indent=2)}

    AI INITIAL FINDINGS:
    [[INITIAL_FINDINGS]]

    Compare these findings against the original code and produce actionable,
    line-specific remediation instructions.

    Your review must:

    1. Consider the static-analysis findings.
    2. Identify additional issues that static analysis may have missed.
    3. Avoid duplicating the same issue unnecessarily.
    4. For every actionable issue, identify the relevant line.
    5. Explain what is wrong.
    6. Tell the developer exactly what they should change.
    7. Provide a small suggested code change where appropriate.
    8. Explain why the change improves the code.
    9. Do not invent problems that are not supported by the code.
    10. Do not rewrite the entire program unless necessary.

    Return ONLY valid JSON using this structure:

    {{
        "summary": "Brief overall assessment",
        "actions": [
            {{
                "line": 1,
                "category": "readability",
                "issue": "What is wrong",
                "action": "What the developer should do",
                "suggested_code": "Optional corrected code",
                "reason": "Why the change should be made"
            }}
        ]
    }}

    If there are no actionable issues, return:

    {{
        "summary": "No actionable remediation was identified.",
        "actions": []
    }}
    """

    if client is None:
        return {
            "tool": "openai",
            "summary": "",
            "issues": [],
            "actions": [],
            "error": "OPENAI_API_KEY is not configured"
        }

    try:
        initial_response_text = _call_openai(initial_prompt)
        initial_result = _load_json_response(initial_response_text)

        if initial_result is None:
            return {
                "tool": "openai",
                "summary": "",
                "issues": [],
                "actions": [],
                "error": "AI returned invalid JSON"
            }

        initial_issues = initial_result.get("issues", [])
        initial_summary = initial_result.get("summary", "")

        remediation_response_text = _call_openai(
            remediation_prompt.replace(
                "[[INITIAL_FINDINGS]]",
                json.dumps(initial_issues, indent=2)
            )
        )
        remediation_result = _load_json_response(remediation_response_text)

        actions = []
        remediation_error = None

        if remediation_result is None:
            remediation_error = "AI returned invalid JSON for remediation guidance"
        else:
            actions = remediation_result.get("actions", [])

        summary = remediation_result.get("summary", initial_summary) if remediation_result else initial_summary

        return {
            "tool": "openai",
            "summary": summary,
            "issues": initial_issues,
            "actions": actions,
            **(
                {"remediation_error": remediation_error}
                if remediation_error
                else {}
            )
        }

    except Exception as error:

        return {
            "tool": "openai",
            "summary": "",
            "issues": [],
            "actions": [],
            "error": str(error)
        }