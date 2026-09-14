import os
import re
import shutil
import subprocess
import tempfile


def detect_target_framework():
    if shutil.which("dotnet") is None:
        return "net8.0"

    try:
        result = subprocess.run(
            ["dotnet", "--list-sdks"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return "net8.0"

    versions = []
    for line in (result.stdout or "").splitlines():
        match = re.search(r"(\d+)\.(\d+)\.(\d+)", line.strip())
        if match:
            versions.append((int(match.group(1)), int(match.group(2)), int(match.group(3))))

    if not versions:
        return "net8.0"

    major = max(version[0] for version in versions)
    return f"net{major}.0"


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

    target_framework = detect_target_framework()

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            create_project = subprocess.run(
                [
                    "dotnet",
                    "new",
                    "console",
                    "--framework",
                    target_framework,
                    "--output",
                    temp_dir
                ],
                capture_output=True,
                text=True,
                timeout=30,
                check=False
            )
        except OSError as exc:
            return {
                "tool": "Roslyn",
                "findings": [],
                "success": False,
                "error": f"Failed to start dotnet: {exc}"
            }
        except subprocess.TimeoutExpired:
            return {
                "tool": "Roslyn",
                "findings": [],
                "success": False,
                "error": "C# project creation timed out while preparing the SDK template."
            }

        if create_project.returncode != 0:
            return {
                "tool": "Roslyn",
                "findings": [],
                "success": False,
                "error": create_project.stderr or create_project.stdout or "Failed to initialise the C# project."
            }

        program_path = os.path.join(temp_dir, "Program.cs")

        try:
            with open(program_path, "w", encoding="utf-8") as file:
                file.write(code)
        except Exception as exc:
            return {
                "tool": "Roslyn",
                "findings": [],
                "success": False,
                "error": f"Failed to write C# program: {exc}"
            }

        try:
            result = subprocess.run(
                [
                    "dotnet",
                    "build",
                    temp_dir,
                    "-nologo",
                    "-v:q"
                ],
                capture_output=True,
                text=True,
                timeout=30,
                check=False
            )
        except subprocess.TimeoutExpired as exc:
            return {
                "tool": "Roslyn",
                "findings": [],
                "success": False,
                "error": "C# analysis timed out after 30 seconds. The .NET build was too slow or resource-constrained."
            }
        except OSError as exc:
            return {
                "tool": "Roslyn",
                "findings": [],
                "success": False,
                "error": f"Failed to run dotnet build: {exc}"
            }

        output = (result.stdout or "") + (result.stderr or "")

        findings = parse_diagnostics(output)

        return {
            "tool": "Roslyn",
            "findings": findings,
            "success": result.returncode == 0,
            "error": None if result.returncode == 0 else output
        }