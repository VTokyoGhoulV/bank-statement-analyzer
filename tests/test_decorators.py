from __future__ import annotations

from datetime import datetime

import pandas as pd

from src import decorators
from src.decorators import report_to_file


def test_report_to_file_returns_non_dataframe_without_writing(tmp_path) -> None:
    output = tmp_path / "unused.json"

    @report_to_file(str(output))
    def build_dict():
        return {"ok": True}

    assert build_dict() == {"ok": True}
    assert not output.exists()


def test_report_to_file_serializes_datetime_and_preserves_metadata(tmp_path, monkeypatch) -> None:
    reports_dir = tmp_path / "data" / "reports"
    reports_dir.mkdir(parents=True)
    monkeypatch.setattr(decorators, "find_project_root", lambda: tmp_path)
    output = reports_dir / "report.json"

    @report_to_file("report")
    def build_report():
        return pd.DataFrame([{"created_at": datetime(2026, 6, 1, 12, 30), "value": 10}])

    result = build_report()
    assert build_report.__name__ == "build_report"
    assert result.loc[0, "created_at"] == "01.06.2026 12:30:00"
    assert "01.06.2026 12:30:00" in output.read_text(encoding="utf-8")
