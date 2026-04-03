import json
import pytest
from unittest.mock import patch

from language_teacher.vocab import display_vocab, get_random_words, get_vocab, search_vocab
from language_teacher.hsk_data import HSK_VOCAB, CATEGORIES


def test_get_vocab_all():
    result = get_vocab()
    assert len(result) == len(HSK_VOCAB)


def test_get_vocab_by_band():
    for band in (1, 2, 3):
        result = get_vocab(band=band)
        assert len(result) > 0
        assert all(w["band"] == band for w in result)


def test_get_vocab_by_category():
    result = get_vocab(category="verb")
    assert len(result) > 0
    assert all(w["category"] == "verb" for w in result)


def test_get_vocab_by_band_and_category():
    result = get_vocab(band=1, category="pronoun")
    assert len(result) > 0
    assert all(w["band"] == 1 and w["category"] == "pronoun" for w in result)


def test_get_vocab_invalid_band():
    result = get_vocab(band=99)
    assert result == []


def test_get_random_words_default():
    result = get_random_words()
    assert len(result) == 10


def test_get_random_words_with_band():
    result = get_random_words(n=5, band=1)
    assert len(result) == 5
    assert all(w["band"] == 1 for w in result)


def test_get_random_words_exceeds_pool():
    pool = get_vocab(band=1)
    result = get_random_words(n=9999, band=1)
    assert len(result) == len(pool)


def test_get_random_words_empty_band():
    result = get_random_words(n=5, band=99)
    assert result == []


def test_search_vocab_english():
    result = search_vocab("I; me")
    assert any(w["hanzi"] == "我" for w in result)


def test_search_vocab_pinyin():
    result = search_vocab("wo3")
    assert any(w["hanzi"] == "我" for w in result)


def test_search_vocab_hanzi():
    result = search_vocab("我")
    assert any(w["hanzi"] == "我" for w in result)


def test_search_vocab_no_match():
    result = search_vocab("xyznonexistent")
    assert result == []


def test_display_vocab_empty(capsys):
    display_vocab([])
    # Should not raise


def test_display_vocab_nonempty():
    words = get_vocab(band=1, category="pronoun")[:3]
    with patch("language_teacher.vocab.Console") as MockConsole:
        instance = MockConsole.return_value
        display_vocab(words, title="Test")
        instance.print.assert_called_once()
