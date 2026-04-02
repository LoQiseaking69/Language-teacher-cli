"""Vocabulary browsing and filtering for HSK word lists."""

import random
from typing import List, Optional

from rich.console import Console
from rich.table import Table

from language_teacher.hsk_data import CATEGORIES, HSK_BANDS, HSK_VOCAB


def get_vocab(
    band: Optional[int] = None,
    category: Optional[str] = None,
) -> List[dict]:
    """Return HSK vocabulary filtered by band and/or category."""
    results = HSK_VOCAB
    if band is not None:
        results = [w for w in results if w["band"] == band]
    if category is not None:
        results = [w for w in results if w["category"] == category]
    return results


def get_random_words(n: int = 10, band: Optional[int] = None) -> List[dict]:
    """Return *n* random words, optionally filtered by band."""
    pool = get_vocab(band=band)
    if not pool:
        return []
    return random.sample(pool, min(n, len(pool)))


def search_vocab(query: str) -> List[dict]:
    """Search vocabulary by English, pinyin, or hanzi substring."""
    q = query.strip().lower()
    return [
        w
        for w in HSK_VOCAB
        if q in w["english"].lower()
        or q in w["pinyin"].lower()
        or q in w["hanzi"]
    ]


def display_vocab(words: List[dict], title: str = "HSK Vocabulary") -> None:
    """Pretty-print a word list using Rich tables."""
    console = Console()
    if not words:
        console.print("[yellow]No matching words found.[/yellow]")
        return

    table = Table(title=title)
    table.add_column("Band", style="cyan", justify="center")
    table.add_column("Hanzi", style="bold green")
    table.add_column("Pinyin", style="magenta")
    table.add_column("English", style="white")
    table.add_column("Category", style="dim")

    for w in words:
        table.add_row(
            str(w["band"]),
            w["hanzi"],
            w["pinyin"],
            w["english"],
            w["category"],
        )

    console.print(table)
