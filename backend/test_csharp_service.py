import importlib


def test_analyse_csharp_reports_missing_dotnet_cleanly(monkeypatch):
    csharp_service = importlib.import_module("services.csharp_service")

    monkeypatch.setattr(csharp_service.shutil, "which", lambda _: None)

    result = csharp_service.analyse_csharp("class Program {}")

    assert result["tool"] == "Roslyn"
    assert result["findings"] == []
    assert result["success"] is False
    assert ".NET SDK" in result["error"]
