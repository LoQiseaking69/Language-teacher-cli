import pytest
from unittest.mock import patch, MagicMock

from language_teacher.translate import translate_text


def _mock_response(status_code=200, json_data=None):
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data or {
        "responseStatus": 200,
        "responseData": {"translatedText": "你好"},
    }
    return mock


def test_translate_success():
    with patch("language_teacher.translate.requests.get", return_value=_mock_response()):
        result = translate_text("hello", "zh-CN")
    assert result == "你好"


def test_translate_http_error():
    with patch("language_teacher.translate.requests.get", return_value=_mock_response(status_code=500)):
        result = translate_text("hello", "zh-CN")
    assert result == "[Translation Error]"


def test_translate_network_error():
    import requests as req
    with patch("language_teacher.translate.requests.get", side_effect=req.exceptions.RequestException("timeout")):
        result = translate_text("hello", "zh-CN")
    assert result.startswith("[Translation Error:")


def test_translate_bad_response_status():
    mock = _mock_response(json_data={"responseStatus": 403, "responseData": {"translatedText": ""}})
    with patch("language_teacher.translate.requests.get", return_value=mock):
        result = translate_text("hello", "zh-CN")
    assert result == "[Translation Error]"


def test_translate_warns_when_result_equals_input(capsys):
    mock = _mock_response(json_data={
        "responseStatus": 200,
        "responseData": {"translatedText": "hello"},
    })
    with patch("language_teacher.translate.requests.get", return_value=mock):
        result = translate_text("hello", "zh-CN")
    captured = capsys.readouterr()
    assert "Warning" in captured.out
    assert result == "hello"
