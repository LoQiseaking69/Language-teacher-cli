"""Interactive typing drill for language practice.

Presents vocabulary words and asks the user to type the correct characters.
Supports Mandarin Chinese (HSK levels 1–6).
"""

from typing import Any, Callable, Dict, List, Optional, Union

import typer
from rich.console import Console
from rich.table import Table

console = Console()


def _normalize(text: str) -> str:
    """Strip whitespace for comparison."""
    return text.strip()


def run_drill(
    words: List[Dict[str, str]],
    speak_fn: Optional[Callable[[str, str], Any]] = None,
    voice: str = "zh-CN-XiaoxiaoNeural",
) -> Dict[str, Union[int, List[Dict[str, str]]]]:
    """Run an interactive typing drill and return results.

    Args:
        words: List of vocabulary dicts with keys ``hanzi``, ``pinyin``, ``english``.
        speak_fn: Optional callable(text, voice) for TTS playback.
        voice: TTS voice identifier.

    Returns:
        Dict with ``total``, ``correct``, ``wrong``, and ``details`` keys.
    """
    total = len(words)
    correct = 0
    details: List[Dict[str, str]] = []

    console.print(
        f"\n[bold cyan]✏️  Typing Drill – {total} words[/bold cyan]\n"
        "Type the Chinese characters for each prompt. Press Ctrl+C to quit early.\n"
    )

    for i, word in enumerate(words, 1):
        console.print(
            f"[bold][{i}/{total}][/bold]  "
            f"[yellow]{word['english']}[/yellow]  "
            f"[dim](pinyin: {word['pinyin']})[/dim]"
        )

        try:
            answer = typer.prompt("  Your answer")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Drill ended early.[/dim]")
            break

        expected = _normalize(word["hanzi"])
        given = _normalize(answer)
        is_correct = given == expected

        if is_correct:
            correct += 1
            console.print("  [green]✓ Correct![/green]\n")
        else:
            console.print(
                f"  [red]✗ Incorrect.[/red]  "
                f"Expected: [bold]{expected}[/bold]\n"
            )

        details.append(
            {
                "english": word["english"],
                "expected": expected,
                "given": given,
                "result": "✓" if is_correct else "✗",
            }
        )

        if speak_fn and callable(speak_fn):
            speak_fn(expected, voice)

    answered = len(details)
    wrong = answered - correct
    pct = (correct / answered * 100) if answered else 0

    # ── Summary table ──
    console.print("[bold cyan]── Results ──[/bold cyan]")
    summary = Table(show_header=True, header_style="bold")
    summary.add_column("Metric", style="white")
    summary.add_column("Value", justify="right")
    summary.add_row("Answered", str(answered))
    summary.add_row("Correct", f"[green]{correct}[/green]")
    summary.add_row("Wrong", f"[red]{wrong}[/red]")
    summary.add_row("Score", f"{pct:.0f}%")
    console.print(summary)

    # ── Detailed breakdown ──
    if details:
        detail_table = Table(title="Drill Details", show_header=True, header_style="bold")
        detail_table.add_column("#", justify="right", style="dim")
        detail_table.add_column("English", style="yellow")
        detail_table.add_column("Expected", style="cyan")
        detail_table.add_column("Your Answer")
        detail_table.add_column("Result", justify="center")
        for idx, d in enumerate(details, 1):
            style = "green" if d["result"] == "✓" else "red"
            detail_table.add_row(
                str(idx),
                d["english"],
                d["expected"],
                f"[{style}]{d['given']}[/{style}]",
                f"[{style}]{d['result']}[/{style}]",
            )
        console.print(detail_table)

    return {
        "total": total,
        "correct": correct,
        "wrong": wrong,
        "details": details,
    }
