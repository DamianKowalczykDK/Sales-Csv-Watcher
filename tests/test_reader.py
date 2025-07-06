from src.io.reader import CsvReader
from pathlib import Path
import pytest

@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    content = "data;value\n2025-06-28;150\n2025-06-29;200"
    file_path = tmp_path / "sample.csv"
    file_path.write_text(content)
    return file_path

def test_reader(sample_csv: Path) -> None:
    reader: CsvReader[str] = CsvReader(delimiter=";")
    res = reader.read(sample_csv, lambda row: row["data"])
    assert "2025-06-28" in res
    assert res["2025-06-28"]["value"] == "150"
