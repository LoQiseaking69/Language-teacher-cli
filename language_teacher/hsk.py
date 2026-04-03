"""HSK vocabulary data for Mandarin Chinese typing practice.

Contains vocabulary for HSK Levels 1–6 based on the classic HSK standard
(pre-2021), organized by level.  Each entry includes simplified Chinese
characters (hanzi), pinyin romanization, and English translation.

The vocabulary covers the ~5 000 core words tested across all six HSK levels
and is suitable for building Mandarin reading and typing skills from
beginner through advanced.
"""

import random
from typing import Dict, List

from language_teacher.hsk_data.level1 import WORDS as _L1
from language_teacher.hsk_data.level2 import WORDS as _L2
from language_teacher.hsk_data.level3 import WORDS as _L3
from language_teacher.hsk_data.level4 import WORDS as _L4
from language_teacher.hsk_data.level5 import WORDS as _L5
from language_teacher.hsk_data.level6 import WORDS as _L6

# Each entry: {"hanzi": str, "pinyin": str, "english": str}
HSK_VOCAB: Dict[int, List[Dict[str, str]]] = {
    1: _L1,
    2: _L2,
    3: _L3,
    4: _L4,
    5: _L5,
    6: _L6,
}

# All HSK levels available in this module
AVAILABLE_LEVELS = sorted(HSK_VOCAB.keys())


def get_words(level: int) -> List[Dict[str, str]]:
    """Return all vocabulary words for a given HSK level."""
    if level not in HSK_VOCAB:
        raise ValueError(
            f"HSK level {level} not available. Choose from: {AVAILABLE_LEVELS}"
        )
    return list(HSK_VOCAB[level])


def get_cumulative_words(level: int) -> List[Dict[str, str]]:
    """Return all vocabulary words up to and including the given HSK level."""
    if level not in HSK_VOCAB:
        raise ValueError(
            f"HSK level {level} not available. Choose from: {AVAILABLE_LEVELS}"
        )
    words: List[Dict[str, str]] = []
    for lvl in AVAILABLE_LEVELS:
        if lvl <= level:
            words.extend(HSK_VOCAB[lvl])
    return words


def get_random_words(level: int, count: int, cumulative: bool = True) -> List[Dict[str, str]]:
    """Return a random selection of words from the given HSK level.

    Args:
        level: HSK level (1–6).
        count: Number of words to return.
        cumulative: If True, include words from all levels up to ``level``.
    """
    pool = get_cumulative_words(level) if cumulative else get_words(level)
    count = min(count, len(pool))
    return random.sample(pool, count)


def word_count(level: int, cumulative: bool = True) -> int:
    """Return the number of words available for a given HSK level."""
    pool = get_cumulative_words(level) if cumulative else get_words(level)
    return len(pool)
