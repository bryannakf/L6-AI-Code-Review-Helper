import subprocess
import tempfile
import os


def analyse_python(code):

    temp_file = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False
        ) as file:

            file.write(code)
            temp_file = file.name

        result = subprocess.run(
            [
                "pylint",
                temp_file,
                "--output-format=json"
            ],
            capture_output=True,
            text=True
        )

        return {
            "tool": "pylint",
            "issues": parse_pylint_output(result.stdout)
        }

    finally:

        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
            
import json


def parse_pylint_output(output):

    try:
        results = json.loads(output)
    except json.JSONDecodeError:
        return []

    issues = []

    for item in results:

        issues.append({
            "type": item.get("type"),
            "message": item.get("message"),
            "line": item.get("line"),
            "column": item.get("column"),
            "symbol": item.get("symbol")
        })

    return issues