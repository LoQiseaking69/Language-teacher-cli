#!/usr/bin/env python3
import typer
from language_teacher.translate import translate_text
from language_teacher.tts import speak_text, list_voices, VOICE_MAP
from language_teacher.config import load_config, save_config
from language_teacher.pinyin_fallback import get_pinyin

app = typer.Typer()
config = load_config()

@app.command()
def teach(text: str = typer.Argument(..., help="English text to translate and speak")):
    lang = config.get("language", "zh-CN")
    voice = config.get("voice", VOICE_MAP.get(lang, "zh-CN-XiaoxiaoNeural"))
    translated = translate_text(text, target_lang=lang)
    pinyin = get_pinyin(translated) if lang.startswith("zh") else ""
    typer.echo(f"[→] Translation: {translated}")
    if pinyin:
        typer.echo(f"[→] Pinyin: {pinyin}")
    speak_text(translated, voice)

@app.command()
def set(lang: str = typer.Argument(..., help="Target language code (e.g., zh-CN, es-ES)"),
        voice: str = typer.Argument(..., help="Edge-TTS voice name for that language")):
    config["language"] = lang
    config["voice"] = voice
    save_config(config)
    typer.echo(f"[✓] Set default language to {lang} with voice {voice}")

@app.command()
def list_voices_cmd():
    list_voices()

if __name__ == "__main__":
    app()
