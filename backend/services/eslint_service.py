import json
import os
import subprocess
import tempfile
from pathlib import Path


def analyse_javascript(code):

    temp_file = None

    try:
        # Find the project root
        project_root = Path(__file__).resolve().parents[2]
        frontend_dir = project_root / "frontend"

        # Choose the correct ESLint executable for the operating system
        if os.name == "nt":
            eslint_path = (
                frontend_dir
                / "node_modules"
                / ".bin"
                / "eslint.cmd"
            )
        else:
            eslint_path = (
                frontend_dir
                / "node_modules"
                / ".bin"
                / "eslint"
            )

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

        result = subprocess.run(
            [
                str(eslint_path),
                temp_file,
                "--format=json"
            ],
            capture_output=True,
            text=True
        )

        # ESLint returns a non-zero exit code when it finds issues.
        # This is expected and should not be treated as a Python error.
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