import pytest

from language_teacher.hsk import (
    AVAILABLE_LEVELS,
    HSK_VOCAB,
    get_cumulative_words,
    get_random_words,
    get_words,
    word_count,
)


def test_available_levels():
    assert AVAILABLE_LEVELS == [1, 2, 3]


def test_get_words_returns_list_for_each_level():
    for level in AVAILABLE_LEVELS:
        words = get_words(level)
        assert isinstance(words, list)
        assert len(words) > 0


def test_get_words_invalid_level():
    with pytest.raises(ValueError, match="not available"):
        get_words(99)


def test_word_structure():
    """Every word must have hanzi, pinyin, and english keys with non-empty values."""
    for level, words in HSK_VOCAB.items():
        for word in words:
            assert "hanzi" in word, f"Missing 'hanzi' in level {level}: {word}"
            assert "pinyin" in word, f"Missing 'pinyin' in level {level}: {word}"
            assert "english" in word, f"Missing 'english' in level {level}: {word}"
            assert word["hanzi"].strip(), f"Empty 'hanzi' in level {level}"
            assert word["pinyin"].strip(), f"Empty 'pinyin' in level {level}"
            assert word["english"].strip(), f"Empty 'english' in level {level}"


def test_no_duplicate_hanzi_within_level():
    """No duplicate hanzi within the same level."""
    for level, words in HSK_VOCAB.items():
        hanzi_set = set()
        for word in words:
            assert word["hanzi"] not in hanzi_set, (
                f"Duplicate hanzi '{word['hanzi']}' in HSK level {level}"
            )
            hanzi_set.add(word["hanzi"])


def test_cumulative_words_includes_lower_levels():
    level1 = get_words(1)
    cumulative2 = get_cumulative_words(2)
    # Cumulative level 2 should include all level 1 words plus level 2 words
    assert len(cumulative2) > len(level1)
    level1_hanzi = {w["hanzi"] for w in level1}
    cumulative2_hanzi = {w["hanzi"] for w in cumulative2}
    assert level1_hanzi.issubset(cumulative2_hanzi)


def test_cumulative_words_level3():
    cumulative3 = get_cumulative_words(3)
    level1_count = len(get_words(1))
    level2_count = len(get_words(2))
    level3_count = len(get_words(3))
    assert len(cumulative3) == level1_count + level2_count + level3_count


def test_get_random_words_count():
    words = get_random_words(1, 5)
    assert len(words) == 5


def test_get_random_words_caps_at_pool_size():
    pool_size = word_count(1, cumulative=False)
    words = get_random_words(1, pool_size + 100, cumulative=False)
    assert len(words) == pool_size


def test_get_random_words_level_only():
    level1_count = word_count(1, cumulative=False)
    words = get_random_words(1, level1_count, cumulative=False)
    assert len(words) == level1_count


def test_word_count():
    for level in AVAILABLE_LEVELS:
        assert word_count(level, cumulative=False) == len(HSK_VOCAB[level])


def test_word_count_cumulative():
    expected = sum(len(HSK_VOCAB[l]) for l in AVAILABLE_LEVELS)
    assert word_count(3, cumulative=True) == expected


def test_minimum_vocabulary_size():
    """HSK3 cumulative vocabulary should be substantial."""
    total = word_count(3, cumulative=True)
    # We should have at least 300 words covering HSK 1-3
    assert total >= 300, f"Expected at least 300 words, got {total}"
