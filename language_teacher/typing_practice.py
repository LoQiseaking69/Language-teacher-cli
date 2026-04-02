"""Interactive typing practice for HSK vocabulary."""

from typing import List, Optional

import typer
from rich.console import Console

from language_teacher.progress import record_attempt
from language_teacher.tts import VOICE_MAP, speak_text
from language_teacher.vocab import get_random_words


def run_typing_practice(
    count: int = 10,
    band: Optional[int] = None,
    no_speak: bool = False,
) -> None:
    """Run an interactive typing practice session.

    The user is shown English + pinyin and must type the correct Chinese characters.
    """
    console = Console()
    words = get_random_words(n=count, band=band)

    if not words:
        console.print("[red]No words available for the selected band.[/red]")
        return

    band_label = f"Band {band}" if band else "All Bands"
    console.print(f"\n[bold]⌨️  HSK Typing Practice — {band_label}[/bold]")
    console.print(f"Type the correct Chinese characters for each prompt.")
    console.print(f"Press Ctrl+C to quit early.\n")

    correct_count = 0
    attempted = 0

    for i, word in enumerate(words, 1):
        console.print(
            f"[cyan]({i}/{len(words)})[/cyan]  "
            f"[white]{word['english']}[/white]  "
            f"[dim]({word['pinyin']})[/dim]"
        )

        try:
            answer = input("  ✏️  Your answer: ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Practice ended early.[/yellow]")
            break

        attempted += 1
        is_correct = answer == word["hanzi"]
        record_attempt(word["hanzi"], is_correct)

        if is_correct:
            correct_count += 1
            console.print(f"  [bold green]✓ Correct![/bold green]\n")
        else:
            console.print(
                f"  [bold red]✗ Incorrect.[/bold red]  "
                f"Answer: [green]{word['hanzi']}[/green]\n"
            )

        if not no_speak:
            try:
                voice = VOICE_MAP.get("zh-CN", "zh-CN-XiaoxiaoNeural")
                speak_text(word["hanzi"], voice)
            except Exception:
                pass  # TTS failure shouldn't stop practice

    if attempted > 0:
        pct = correct_count / attempted * 100
        console.print(
            f"[bold]Score: {correct_count}/{attempted} ({pct:.0f}%)[/bold]\n"
        )


def run_quiz(
    count: int = 10,
    band: Optional[int] = None,
) -> None:
    """Run a review quiz: show Chinese, user types English."""
    console = Console()
    words = get_random_words(n=count, band=band)

    if not words:
        console.print("[red]No words available for the selected band.[/red]")
        return

    band_label = f"Band {band}" if band else "All Bands"
    console.print(f"\n[bold]📝 HSK Quiz — {band_label}[/bold]")
    console.print(f"Type the English meaning for each Chinese word.")
    console.print(f"Press Ctrl+C to quit early.\n")

    correct_count = 0
    attempted = 0

    for i, word in enumerate(words, 1):
        console.print(
            f"[cyan]({i}/{len(words)})[/cyan]  "
            f"[bold green]{word['hanzi']}[/bold green]  "
            f"[dim]({word['pinyin']})[/dim]"
        )

        try:
            answer = input("  ✏️  English meaning: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Quiz ended early.[/yellow]")
            break

        attempted += 1
        expected = word["english"].lower()
        # Accept if the answer is a substring match or vice versa
        is_correct = answer == expected or answer in expected or expected in answer
        record_attempt(word["hanzi"], is_correct)

        if is_correct:
            correct_count += 1
            console.print(f"  [bold green]✓ Correct![/bold green]\n")
        else:
            console.print(
                f"  [bold red]✗ Incorrect.[/bold red]  "
                f"Answer: [white]{word['english']}[/white]\n"
            )

    if attempted > 0:
        pct = correct_count / attempted * 100
        console.print(
            f"[bold]Score: {correct_count}/{attempted} ({pct:.0f}%)[/bold]\n"
        )
