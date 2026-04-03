from language_teacher.hsk_data import HSK_VOCAB, HSK_BANDS, CATEGORIES


def test_hsk_vocab_not_empty():
    assert len(HSK_VOCAB) > 0


def test_hsk_vocab_minimum_count():
    """The dataset should have at least 450 words (150 per band)."""
    assert len(HSK_VOCAB) >= 450


def test_all_bands_present():
    bands_found = {w["band"] for w in HSK_VOCAB}
    assert bands_found == {1, 2, 3}


def test_each_band_has_words():
    for band in (1, 2, 3):
        count = sum(1 for w in HSK_VOCAB if w["band"] == band)
        assert count >= 100, f"Band {band} has only {count} words"


def test_required_keys():
    required = {"hanzi", "pinyin", "english", "band", "category"}
    for word in HSK_VOCAB:
        assert required.issubset(word.keys()), f"Missing keys in: {word}"


def test_categories_valid():
    for word in HSK_VOCAB:
        assert word["category"] in CATEGORIES, (
            f"Invalid category '{word['category']}' for {word['hanzi']}"
        )


def test_bands_valid():
    for word in HSK_VOCAB:
        assert word["band"] in HSK_BANDS, (
            f"Invalid band {word['band']} for {word['hanzi']}"
        )


def test_no_duplicate_hanzi():
    seen = set()
    for word in HSK_VOCAB:
        assert word["hanzi"] not in seen, f"Duplicate hanzi: {word['hanzi']}"
        seen.add(word["hanzi"])


def test_hsk_bands_dict():
    assert 1 in HSK_BANDS
    assert 2 in HSK_BANDS
    assert 3 in HSK_BANDS


def test_categories_list():
    assert "noun" in CATEGORIES
    assert "verb" in CATEGORIES
    assert "adjective" in CATEGORIES
