import pytest
from unittest.mock import patch, MagicMock

from language_teacher.drill import run_drill, _normalize


# ── Helpers ──

SAMPLE_WORDS = [
    {"hanzi": "你好", "pinyin": "nǐ hǎo", "english": "hello"},
    {"hanzi": "谢谢", "pinyin": "xièxie", "english": "thank you"},
    {"hanzi": "再见", "pinyin": "zàijiàn", "english": "goodbye"},
]


# ── Unit tests ──

def test_normalize_strips_whitespace():
    assert _normalize("  你好 ") == "你好"
    assert _normalize("hello") == "hello"


def test_drill_all_correct():
    """User answers all correctly → score is 100%."""
    answers = iter(["你好", "谢谢", "再见"])
    with patch("language_teacher.drill.typer.prompt", side_effect=answers):
        result = run_drill(SAMPLE_WORDS)

    assert result["total"] == 3
    assert result["correct"] == 3
    assert result["wrong"] == 0
    assert len(result["details"]) == 3
    assert all(d["result"] == "✓" for d in result["details"])


def test_drill_all_wrong():
    """User answers all incorrectly → score is 0%."""
    answers = iter(["xxx", "yyy", "zzz"])
    with patch("language_teacher.drill.typer.prompt", side_effect=answers):
        result = run_drill(SAMPLE_WORDS)

    assert result["correct"] == 0
    assert result["wrong"] == 3
    assert all(d["result"] == "✗" for d in result["details"])


def test_drill_partial():
    """User gets some right and some wrong."""
    answers = iter(["你好", "wrong", "再见"])
    with patch("language_teacher.drill.typer.prompt", side_effect=answers):
        result = run_drill(SAMPLE_WORDS)

    assert result["correct"] == 2
    assert result["wrong"] == 1


def test_drill_early_exit_keyboard_interrupt():
    """User presses Ctrl+C after the first word."""
    with patch("language_teacher.drill.typer.prompt", side_effect=["你好", KeyboardInterrupt]):
        result = run_drill(SAMPLE_WORDS)

    assert result["total"] == 3
    assert len(result["details"]) == 1
    assert result["correct"] == 1


def test_drill_early_exit_eof():
    """User sends EOF after the first word."""
    with patch("language_teacher.drill.typer.prompt", side_effect=["你好", EOFError]):
        result = run_drill(SAMPLE_WORDS)

    assert len(result["details"]) == 1


def test_drill_with_speak_fn():
    """TTS speak function is called with expected hanzi and voice."""
    mock_speak = MagicMock()
    answers = iter(["你好", "谢谢", "再见"])
    with patch("language_teacher.drill.typer.prompt", side_effect=answers):
        run_drill(SAMPLE_WORDS, speak_fn=mock_speak, voice="test-voice")

    assert mock_speak.call_count == 3
    mock_speak.assert_any_call("你好", "test-voice")
    mock_speak.assert_any_call("谢谢", "test-voice")
    mock_speak.assert_any_call("再见", "test-voice")


def test_drill_no_speak_fn():
    """No errors when speak_fn is None."""
    answers = iter(["你好", "谢谢", "再见"])
    with patch("language_teacher.drill.typer.prompt", side_effect=answers):
        result = run_drill(SAMPLE_WORDS, speak_fn=None)

    assert result["correct"] == 3


def test_drill_empty_word_list():
    """Drill with no words should return zero results."""
    result = run_drill([])
    assert result["total"] == 0
    assert result["correct"] == 0
    assert result["wrong"] == 0
    assert result["details"] == []
