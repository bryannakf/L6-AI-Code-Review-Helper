import importlib
import subprocess


def test_analyse_csharp_reports_missing_dotnet_cleanly(monkeypatch):
    csharp_service = importlib.import_module("services.csharp_service")

    monkeypatch.setattr(csharp_service.shutil, "which", lambda _: None)

    result = csharp_service.analyse_csharp("class Program {}")

    assert result["tool"] == "Roslyn"
    assert result["findings"] == []
    assert result["success"] is False
    assert ".NET SDK" in result["error"]


def test_analyse_csharp_handles_timeout_cleanly(monkeypatch):
    csharp_service = importlib.import_module("services.csharp_service")

    monkeypatch.setattr(csharp_service.shutil, "which", lambda _: "/usr/bin/dotnet")

    def fake_run(command, *args, **kwargs):
        if command[:2] == ["dotnet", "new"]:
            return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        if command[:2] == ["dotnet", "build"]:
            raise subprocess.TimeoutExpired(cmd="dotnet build", timeout=30)
        return type("Result", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    monkeypatch.setattr(csharp_service.subprocess, "run", fake_run)

    result = csharp_service.analyse_csharp("class Program {}")

    assert result["tool"] == "Roslyn"
    assert result["findings"] == []
    assert result["success"] is False
    assert "timed out" in result["error"].lower()
