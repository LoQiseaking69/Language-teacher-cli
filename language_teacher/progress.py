"""Progress tracking for HSK vocabulary practice."""

import json
import os
from typing import Any, Dict

from rich.console import Console
from rich.table import Table

from language_teacher.hsk_data import HSK_BANDS, HSK_VOCAB

PROGRESS_PATH = os.path.expanduser("~/.language_teacher_progress.json")


def load_progress() -> Dict[str, Any]:
    """Load progress data from disk."""
    if not os.path.exists(PROGRESS_PATH):
        return {}
    try:
        with open(PROGRESS_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_progress(data: Dict[str, Any]) -> None:
    """Persist progress data to disk."""
    try:
        with open(PROGRESS_PATH, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"[!] Could not save progress: {e}")


def record_attempt(hanzi: str, correct: bool) -> None:
    """Record a single practice attempt for a word."""
    data = load_progress()
    entry = data.get(hanzi, {"attempts": 0, "correct": 0})
    entry["attempts"] = entry.get("attempts", 0) + 1
    if correct:
        entry["correct"] = entry.get("correct", 0) + 1
    data[hanzi] = entry
    save_progress(data)


def show_progress() -> None:
    """Display a summary of learning progress."""
    data = load_progress()
    console = Console()

    if not data:
        console.print("[yellow]No practice history yet. Try 'language-teacher typing-practice'![/yellow]")
        return

    total_attempted = len(data)
    total_correct = sum(1 for e in data.values() if e.get("correct", 0) > 0)
    total_mastered = sum(
        1 for e in data.values()
        if e.get("attempts", 0) >= 3 and e.get("correct", 0) / e.get("attempts", 1) >= 0.8
    )

    console.print(f"\n[bold]📊 HSK Learning Progress[/bold]")
    console.print(f"  Words attempted : [cyan]{total_attempted}[/cyan] / {len(HSK_VOCAB)}")
    console.print(f"  Words correct   : [green]{total_correct}[/green]")
    console.print(f"  Words mastered  : [bold green]{total_mastered}[/bold green]  (≥80% over 3+ attempts)")

    # Per-band breakdown
    table = Table(title="Progress by Band")
    table.add_column("Band", style="cyan")
    table.add_column("Attempted", justify="right")
    table.add_column("Total", justify="right")
    table.add_column("Mastered", justify="right", style="green")

    for band_num, band_name in HSK_BANDS.items():
        band_hanzi = {w["hanzi"] for w in HSK_VOCAB if w["band"] == band_num}
        attempted = sum(1 for h in band_hanzi if h in data)
        mastered = sum(
            1
            for h in band_hanzi
            if h in data
            and data[h].get("attempts", 0) >= 3
            and data[h].get("correct", 0) / data[h].get("attempts", 1) >= 0.8
        )
        table.add_row(band_name, str(attempted), str(len(band_hanzi)), str(mastered))

    console.print(table)
