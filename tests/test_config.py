import json
import os
import pytest
from unittest.mock import patch, mock_open

from language_teacher.config import load_config, save_config


def test_load_config_missing_file(tmp_path):
    path = str(tmp_path / "config.json")
    with patch("language_teacher.config.CONFIG_PATH", path):
        result = load_config()
    assert result == {}


def test_load_config_valid(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"language": "es-ES", "voice": "es-ES-ElviraNeural"}))
    with patch("language_teacher.config.CONFIG_PATH", str(path)):
        result = load_config()
    assert result == {"language": "es-ES", "voice": "es-ES-ElviraNeural"}


def test_load_config_corrupted(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("not valid json{{")
    with patch("language_teacher.config.CONFIG_PATH", str(path)):
        result = load_config()
    assert result == {}


def test_load_config_strips_unknown_keys(tmp_path):
    path = tmp_path / "config.json"
    path.write_text(json.dumps({"language": "fr-FR", "unknown_key": "value"}))
    with patch("language_teacher.config.CONFIG_PATH", str(path)):
        result = load_config()
    assert "unknown_key" not in result
    assert result["language"] == "fr-FR"


def test_save_config_writes_json(tmp_path):
    path = tmp_path / "config.json"
    with patch("language_teacher.config.CONFIG_PATH", str(path)):
        save_config({"language": "zh-CN", "voice": "zh-CN-XiaoxiaoNeural"})
    data = json.loads(path.read_text())
    assert data["language"] == "zh-CN"
    assert data["voice"] == "zh-CN-XiaoxiaoNeural"


def test_save_config_strips_unknown_keys(tmp_path):
    path = tmp_path / "config.json"
    with patch("language_teacher.config.CONFIG_PATH", str(path)):
        save_config({"language": "zh-CN", "evil_key": "evil"})
    data = json.loads(path.read_text())
    assert "evil_key" not in data


def test_save_config_handles_write_error(capsys):
    with patch("language_teacher.config.CONFIG_PATH", "/nonexistent_dir/config.json"):
        save_config({"language": "zh-CN"})
    captured = capsys.readouterr()
    assert "[!]" in captured.out
