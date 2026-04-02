import json
import pytest
from unittest.mock import patch

from language_teacher.history import log_entry, show_history


def test_log_entry_writes_jsonl(tmp_path):
    history_file = tmp_path / "history.jsonl"
    with patch("language_teacher.history.HISTORY_PATH", str(history_file)):
        log_entry("hello", "你好", "zh-CN", "zh-CN-XiaoxiaoNeural")

    lines = history_file.read_text().strip().splitlines()
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["source"] == "hello"
    assert entry["translated"] == "你好"
    assert entry["lang"] == "zh-CN"
    assert entry["voice"] == "zh-CN-XiaoxiaoNeural"
    assert "timestamp" in entry


def test_log_entry_appends(tmp_path):
    history_file = tmp_path / "history.jsonl"
    with patch("language_teacher.history.HISTORY_PATH", str(history_file)):
        log_entry("hello", "你好", "zh-CN", "zh-CN-XiaoxiaoNeural")
        log_entry("goodbye", "再见", "zh-CN", "zh-CN-XiaoxiaoNeural")

    lines = history_file.read_text().strip().splitlines()
    assert len(lines) == 2


def test_log_entry_handles_write_error(capsys):
    with patch("language_teacher.history.HISTORY_PATH", "/nonexistent_dir/history.jsonl"):
        log_entry("hello", "你好", "zh-CN", "zh-CN-XiaoxiaoNeural")
    captured = capsys.readouterr()
    assert "[!]" in captured.out


def test_show_history_no_file(tmp_path, capsys):
    missing = str(tmp_path / "no_history.jsonl")
    with patch("language_teacher.history.HISTORY_PATH", missing):
        show_history()
    captured = capsys.readouterr()
    assert "No history yet" in captured.out


def test_show_history_displays_entries(tmp_path):
    history_file = tmp_path / "history.jsonl"
    entries = [
        {"timestamp": "2024-01-01T00:00:00+00:00", "source": "hi", "translated": "嗨", "lang": "zh-CN", "voice": "v1"},
        {"timestamp": "2024-01-02T00:00:00+00:00", "source": "bye", "translated": "再见", "lang": "zh-CN", "voice": "v1"},
    ]
    with open(history_file, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")

    with patch("language_teacher.history.HISTORY_PATH", str(history_file)):
        with patch("rich.console.Console.print") as mock_print:
            show_history(n=20)
            mock_print.assert_called_once()


def test_show_history_limits_to_n(tmp_path):
    history_file = tmp_path / "history.jsonl"
    with open(history_file, "w") as f:
        for i in range(10):
            entry = {"timestamp": "2024-01-01T00:00:00+00:00", "source": f"word{i}",
                     "translated": f"译{i}", "lang": "zh-CN", "voice": "v1"}
            f.write(json.dumps(entry) + "\n")

    with patch("language_teacher.history.HISTORY_PATH", str(history_file)):
        with patch("language_teacher.history.Console") as MockConsole:
            instance = MockConsole.return_value
            show_history(n=3)
            table_arg = instance.print.call_args[0][0]
            assert len(table_arg.rows) == 3
