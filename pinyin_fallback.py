def get_pinyin(text):
    try:
        from pypinyin import lazy_pinyin
        return " ".join(lazy_pinyin(text))
    except ImportError:
        return "[pinyin unavailable]"
