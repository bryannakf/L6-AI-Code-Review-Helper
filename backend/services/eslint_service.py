import json
import os
import subprocess
import tempfile
from pathlib import Path


def analyse_javascript(code):

    temp_file = None

    try:
        # Find the frontend directory
        project_root = Path(__file__).resolve().parents[2]
        frontend_dir = project_root / "frontend"

        # Create temporary JavaScript file inside frontend
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".js",
            delete=False,
            dir=frontend_dir,
            encoding="utf-8"
        ) as file:

            file.write(code)
            temp_file = file.name

        eslint_path = (
            frontend_dir
            / "node_modules"
            / ".bin"
            / "eslint.cmd"
        )

        result = subprocess.run(
            [
                str(eslint_path),
                temp_file,
                "--format=json"
            ],
            capture_output=True,
            text=True
        )

        # ESLint can return a non-zero exit code when it finds issues.
        # That is expected and should not be treated as a Python error.
        output = result.stdout or result.stderr

        return {
            "tool": "eslint",
            "issues": parse_eslint_output(output)
        }

    finally:

        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)


def parse_eslint_output(output):

    try:
        results = json.loads(output)
    except (json.JSONDecodeError, TypeError):
        return []

    issues = []

    for item in results[0].get("messages", []):

        issues.append({
            "type": item.get("severity"),
            "message": item.get("message"),
            "line": item.get("line"),
            "column": item.get("column"),
            "ruleId": item.get("ruleId")
        })

    return issues
