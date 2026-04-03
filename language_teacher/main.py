#!/usr/bin/env python3
from typing import Optional

import typer

from language_teacher.config import load_config, save_config
from language_teacher.history import log_entry, show_history
from language_teacher.hsk_data import CATEGORIES, HSK_BANDS, HSK_VOCAB
from language_teacher.pinyin_fallback import get_pinyin
from language_teacher.progress import show_progress
from language_teacher.translate import translate_text
from language_teacher.tts import VOICE_MAP, list_voices, speak_text
from language_teacher.typing_practice import run_quiz, run_typing_practice
from language_teacher.vocab import display_vocab, get_vocab, search_vocab

app = typer.Typer(help="Language Teacher CLI – translate, speak, and practice typing in foreign languages")
config = load_config()


# ---------------------------------------------------------------------------
# Existing commands
# ---------------------------------------------------------------------------


@app.command()
def teach(
    text: str = typer.Argument(..., help="English text to translate and speak"),
    no_speak: bool = typer.Option(False, "--no-speak", help="Skip TTS playback"),
):
    """Translate English text and speak it in the target language."""
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
    """Set the default target language and TTS voice."""
    config["language"] = lang
    config["voice"] = voice
    save_config(config)
    typer.echo(f"[✓] Set default language to {lang} with voice {voice}")


@app.command(name="list-voices")
def list_voices_cmd():
    """Show all available Edge-TTS voices."""
    list_voices()


@app.command()
def history(n: int = typer.Option(20, help="Number of recent entries to show")):
    """Show your past translated sentences."""
    show_history(n)


# ---------------------------------------------------------------------------
# HSK vocabulary & practice commands
# ---------------------------------------------------------------------------


@app.command()
def vocab(
    band: Optional[int] = typer.Option(None, "--band", "-b", help="HSK band (1, 2, or 3)"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Part-of-speech category"),
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Search by English, pinyin, or hanzi"),
):
    """Browse HSK 1-3 vocabulary lists."""
    if search:
        words = search_vocab(search)
        title = f"Search results for '{search}'"
    else:
        words = get_vocab(band=band, category=category)
        parts = []
        if band:
            parts.append(f"Band {band}")
        if category:
            parts.append(category)
        title = "HSK Vocabulary" + (f" — {', '.join(parts)}" if parts else "")
    display_vocab(words, title=title)


@app.command(name="typing-practice")
def typing_practice_cmd(
    count: int = typer.Option(10, "--count", "-n", help="Number of words to practice"),
    band: Optional[int] = typer.Option(None, "--band", "-b", help="HSK band (1, 2, or 3)"),
    no_speak: bool = typer.Option(False, "--no-speak", help="Skip TTS playback"),
):
    """Practice typing Chinese characters from English/pinyin prompts."""
    run_typing_practice(count=count, band=band, no_speak=no_speak)


@app.command()
def quiz(
    count: int = typer.Option(10, "--count", "-n", help="Number of words to quiz"),
    band: Optional[int] = typer.Option(None, "--band", "-b", help="HSK band (1, 2, or 3)"),
):
    """Quiz: type the English meaning for Chinese words."""
    run_quiz(count=count, band=band)


@app.command()
def progress():
    """Show your HSK vocabulary learning progress."""
    show_progress()


@app.command(name="hsk-info")
def hsk_info():
    """Display information about available HSK bands and categories."""
    typer.echo("[📚] HSK Bands:")
    for num, name in HSK_BANDS.items():
        count = sum(1 for w in HSK_VOCAB if w["band"] == num)
        typer.echo(f"  Band {num}: {name} ({count} words)")

    typer.echo(f"\n[📂] Categories: {', '.join(CATEGORIES)}")
    typer.echo(f"\n[Σ] Total vocabulary: {len(HSK_VOCAB)} words")


if __name__ == "__main__":
    app()
