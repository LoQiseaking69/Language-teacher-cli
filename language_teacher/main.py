#!/usr/bin/env python3
import typer

from language_teacher.config import load_config, save_config
from language_teacher.drill import run_drill
from language_teacher.history import log_entry, show_history
from language_teacher.hsk import AVAILABLE_LEVELS, get_random_words, word_count
from language_teacher.pinyin_fallback import get_pinyin
from language_teacher.translate import translate_text
from language_teacher.tts import VOICE_MAP, list_voices, speak_text

app = typer.Typer(help="Language Teacher CLI – translate and speak text in foreign languages")
config = load_config()


@app.command()
def teach(
    text: str = typer.Argument(..., help="English text to translate and speak"),
    no_speak: bool = typer.Option(False, "--no-speak", help="Skip TTS playback"),
):
    lang = config.get("language", "zh-CN")
    voice = config.get("voice", VOICE_MAP.get(lang, "zh-CN-XiaoxiaoNeural"))
    translated = translate_text(text, target_lang=lang)

    if translated.startswith("["):
        typer.echo(f"[!] {translated}", err=True)
        raise typer.Exit(code=1)

    pinyin = get_pinyin(translated) if lang.startswith("zh") else ""
    typer.echo(f"[→] Translation: {translated}")
    if pinyin:
        typer.echo(f"[→] Pinyin: {pinyin}")

    log_entry(text, translated, lang, voice)

    if not no_speak:
        speak_text(translated, voice)


@app.command()
def set(
    lang: str = typer.Argument(..., help="Target language code (e.g., zh-CN, es-ES)"),
    voice: str = typer.Argument(..., help="Edge-TTS voice name for that language"),
):
    config["language"] = lang
    config["voice"] = voice
    save_config(config)
    typer.echo(f"[✓] Set default language to {lang} with voice {voice}")


@app.command(name="list-voices")
def list_voices_cmd():
    list_voices()


@app.command()
def history(n: int = typer.Option(20, help="Number of recent entries to show")):
    show_history(n)


@app.command()
def drill(
    level: int = typer.Option(3, "--level", "-l", help="HSK level (1–6)"),
    count: int = typer.Option(10, "--count", "-c", help="Number of words per session (min 1)"),
    no_speak: bool = typer.Option(False, "--no-speak", help="Skip TTS playback"),
    cumulative: bool = typer.Option(
        True, "--cumulative/--level-only",
        help="Include words from lower HSK levels",
    ),
):
    """Practice typing Mandarin Chinese characters (HSK 1–6)."""
    if count < 1:
        typer.echo("[!] --count must be at least 1.", err=True)
        raise typer.Exit(code=1)

    if level not in AVAILABLE_LEVELS:
        typer.echo(
            f"[!] Invalid HSK level {level}. Choose from: {AVAILABLE_LEVELS}",
            err=True,
        )
        raise typer.Exit(code=1)

    total_available = word_count(level, cumulative=cumulative)
    actual_count = min(count, total_available)
    words = get_random_words(level, actual_count, cumulative=cumulative)

    voice = config.get("voice", VOICE_MAP.get("zh-CN", "zh-CN-XiaoxiaoNeural"))
    speak_fn = None if no_speak else speak_text

    run_drill(words, speak_fn=speak_fn, voice=voice)


@app.command(name="hsk-info")
def hsk_info(
    level: int = typer.Option(3, "--level", "-l", help="HSK level (1–6)"),
):
    """Show HSK vocabulary statistics and sample words."""
    from rich.console import Console
    from rich.table import Table

    if level not in AVAILABLE_LEVELS:
        typer.echo(
            f"[!] Invalid HSK level {level}. Choose from: {AVAILABLE_LEVELS}",
            err=True,
        )
        raise typer.Exit(code=1)

    con = Console()
    con.print(f"\n[bold cyan]HSK Level {level} Vocabulary Info[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Level")
    table.add_column("Words (this level)", justify="right")
    table.add_column("Words (cumulative)", justify="right")

    for lvl in AVAILABLE_LEVELS:
        if lvl <= level:
            this_lvl = word_count(lvl, cumulative=False)
            cumul = word_count(lvl, cumulative=True)
            table.add_row(f"HSK {lvl}", str(this_lvl), str(cumul))

    con.print(table)
    con.print(
        f"\nUse [bold]language-teacher drill --level {level}[/bold] "
        "to start a typing practice session.\n"
    )


if __name__ == "__main__":
    app()
