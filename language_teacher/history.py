import json
import os
from datetime import datetime, timezone

from rich.console import Console
from rich.table import Table

HISTORY_PATH = os.path.expanduser("~/.language_teacher_history.jsonl")


def log_entry(source: str, translated: str, lang: str, voice: str) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "translated": translated,
        "lang": lang,
        "voice": voice,
    }
    try:
        with open(HISTORY_PATH, "a") as f:
            print(json.dumps(entry), file=f)
    except OSError as e:
        print(f"[!] Could not write history: {e}")


def show_history(n: int = 20) -> None:
    if not os.path.exists(HISTORY_PATH):
        print("No history yet.")
        return

    try:
        with open(HISTORY_PATH, "r") as f:
            lines = f.readlines()
    except OSError as e:
        print(f"[!] Could not read history: {e}")
        return

    recent = lines[-n:]
    console = Console()
    table = Table(title="Translation History")
    table.add_column("Timestamp", style="dim")
    table.add_column("Lang", style="cyan")
    table.add_column("Source", style="white")
    table.add_column("Translation", style="green")

    for line in recent:
        try:
            entry = json.loads(line)
            table.add_row(
                entry.get("timestamp", ""),
                entry.get("lang", ""),
                entry.get("source", ""),
                entry.get("translated", ""),
            )
        except json.JSONDecodeError:
            continue

    console.print(table)
