import json
import pytest
from unittest.mock import patch

from language_teacher.progress import (
    load_progress,
    save_progress,
    record_attempt,
    show_progress,
    PROGRESS_PATH,
)


def test_load_progress_missing_file(tmp_path):
    path = str(tmp_path / "progress.json")
    with patch("language_teacher.progress.PROGRESS_PATH", path):
        result = load_progress()
    assert result == {}


def test_load_progress_valid(tmp_path):
    path = tmp_path / "progress.json"
    data = {"我": {"attempts": 3, "correct": 2}}
    path.write_text(json.dumps(data))
    with patch("language_teacher.progress.PROGRESS_PATH", str(path)):
        result = load_progress()
    assert result == data


def test_load_progress_corrupted(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text("not valid json{{{")
    with patch("language_teacher.progress.PROGRESS_PATH", str(path)):
        result = load_progress()
    assert result == {}


def test_save_progress(tmp_path):
    path = tmp_path / "progress.json"
    data = {"你": {"attempts": 1, "correct": 1}}
    with patch("language_teacher.progress.PROGRESS_PATH", str(path)):
        save_progress(data)
    saved = json.loads(path.read_text())
    assert saved == data


def test_save_progress_handles_write_error(capsys):
    with patch("language_teacher.progress.PROGRESS_PATH", "/nonexistent_dir/progress.json"):
        save_progress({"x": {"attempts": 1, "correct": 0}})
    captured = capsys.readouterr()
    assert "[!]" in captured.out


def test_record_attempt_correct(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text("{}")
    with patch("language_teacher.progress.PROGRESS_PATH", str(path)):
        record_attempt("好", True)
    saved = json.loads(path.read_text())
    assert saved["好"]["attempts"] == 1
    assert saved["好"]["correct"] == 1


def test_record_attempt_incorrect(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text("{}")
    with patch("language_teacher.progress.PROGRESS_PATH", str(path)):
        record_attempt("好", False)
    saved = json.loads(path.read_text())
    assert saved["好"]["attempts"] == 1
    assert saved["好"]["correct"] == 0


def test_record_attempt_increments(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text("{}")
    with patch("language_teacher.progress.PROGRESS_PATH", str(path)):
        record_attempt("好", True)
        record_attempt("好", False)
        record_attempt("好", True)
    saved = json.loads(path.read_text())
    assert saved["好"]["attempts"] == 3
    assert saved["好"]["correct"] == 2


def test_show_progress_empty(tmp_path):
    path = str(tmp_path / "progress.json")
    with patch("language_teacher.progress.PROGRESS_PATH", path):
        with patch("language_teacher.progress.Console") as MockConsole:
            show_progress()
            instance = MockConsole.return_value
            instance.print.assert_called()


def test_show_progress_with_data(tmp_path):
    path = tmp_path / "progress.json"
    data = {"我": {"attempts": 5, "correct": 4}, "你": {"attempts": 3, "correct": 3}}
    path.write_text(json.dumps(data))
    with patch("language_teacher.progress.PROGRESS_PATH", str(path)):
        with patch("language_teacher.progress.Console") as MockConsole:
            show_progress()
            instance = MockConsole.return_value
            assert instance.print.call_count >= 1
