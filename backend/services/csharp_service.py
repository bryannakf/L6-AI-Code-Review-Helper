import os
import re
import shutil
import subprocess
import tempfile


def parse_diagnostics(output):
    findings = []

    pattern = re.compile(
        r"(?P<file>.+?)\((?P<line>\d+),(?P<column>\d+)\): "
        r"(?P<severity>error|warning|info) "
        r"(?P<rule>[A-Z]+\d+): "
        r"(?P<message>.*)"
    )

    seen = set()

    for line in output.splitlines():

        match = pattern.search(line)

        if not match:
            continue

        message = match.group("message").strip()

        # Remove the temporary .csproj path from the message
        message = re.sub(
            r"\s*\[.*?\.csproj\]",
            "",
            message
        )

        finding = {
            "tool": "Roslyn",
            "message": message,
            "severity": match.group("severity").lower(),
            "line": int(match.group("line")),
            "column": int(match.group("column")),
            "rule": match.group("rule")
        }

        # Prevent duplicate diagnostics
        finding_id = (
            finding["rule"],
            finding["line"],
            finding["column"],
            finding["message"]
        )

        if finding_id not in seen:
            seen.add(finding_id)
            findings.append(finding)

    return findings


def analyse_csharp(code):
    if shutil.which("dotnet") is None:
        return {
            "tool": "Roslyn",
            "findings": [],
            "success": False,
            "error": "The .NET SDK is not installed or not available on PATH. C# analysis cannot run in this environment."
        }

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Create temporary C# project
            create_project = subprocess.run(
                [
                    "dotnet",
                    "new",
                    "console",
                    "--output",
                    temp_dir
                ],
                capture_output=True,
                text=True
            )
        except OSError as exc:
            return {
                "tool": "Roslyn",
                "findings": [],
                "success": False,
                "error": f"Failed to start dotnet: {exc}"
            }

        if create_project.returncode != 0:
            return {
                "tool": "Roslyn",
                "findings": [],
                "success": False,
                "error": create_project.stderr or create_project.stdout or "Failed to initialise the C# project."
            }

        # Replace the generated Program.cs
        program_path = os.path.join(temp_dir, "Program.cs")

        with open(program_path, "w", encoding="utf-8") as file:
            file.write(code)

        try:
            # Run Roslyn/.NET analyzers
            result = subprocess.run(
                [
                    "dotnet",
                    "build",
                    temp_dir,
                    "--no-restore"
                ],
                capture_output=True,
                text=True
            )
        except OSError as exc:
            return {
                "tool": "Roslyn",
                "findings": [],
                "success": False,
                "error": f"Failed to run dotnet build: {exc}"
            }

        output = result.stdout + result.stderr

        findings = parse_diagnostics(output)

        return {
            "tool": "Roslyn",
            "findings": findings,
            "success": result.returncode == 0,
            "error": None if result.returncode == 0 else output
        }