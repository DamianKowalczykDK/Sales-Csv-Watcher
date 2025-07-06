from src.config import parse_arguments, setup_logging
from _pytest.monkeypatch import MonkeyPatch
from pathlib import Path
import logging
import sys

def test_parse_arguments_default(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["program"])
    args = parse_arguments()

    assert args.dir == Path("./data")
    assert args.logfile == "sales.log"
    assert args.key_name == "hour"

def test_setup_logging(tmp_path: Path) -> None:
    log_file = tmp_path / "logs" / "sales.log"
    setup_logging(log_file)

    logger = logging.getLogger()
    logger.info("Test message")

    for handler in logger.handlers:
        if hasattr(handler, "flush"):
            handler.flush()

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "Test message" in content


