import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from the backend/.env file when running locally
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyse_code(code, language):
    """
    Analyse submitted code using OpenAI.

    Returns structured issues identified by the AI.
    """

    prompt = f"""
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
        "issues": []
    }}

    Code to review:

    ```{language}
    {code}
    """
    try:

        response = client.chat.completions.create(
            model="gpt-5.6-luna",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_text = response.choices[0].message.content

        try:
            result = json.loads(response_text)

        except json.JSONDecodeError:

            return {
                "tool": "openai",
                "issues": [],
                "error": "AI returned invalid JSON"
            }

        return {
            "tool": "openai",
            "issues": result.get("issues", [])
        }

    except Exception as error:

        return {
            "tool": "openai",
            "issues": [],
            "error": str(error)
        }