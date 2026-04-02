#!/usr/bin/env python3
import typer

from language_teacher.config import load_config, save_config
from language_teacher.history import log_entry, show_history
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


if __name__ == "__main__":
    app()
