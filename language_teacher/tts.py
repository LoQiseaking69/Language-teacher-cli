import os
import subprocess
from tempfile import NamedTemporaryFile

from rich.console import Console
from rich.table import Table

VOICE_MAP = {
    "zh-CN": "zh-CN-XiaoxiaoNeural",
    "zh-HK": "zh-HK-HiuGaaiNeural",
    "es-ES": "es-ES-ElviraNeural",
    "en-US": "en-US-JennyNeural",
    "fr-FR": "fr-FR-DeniseNeural",
}


def speak_text(text: str, voice: str) -> None:
    with NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        mp3_path = temp_audio.name
    try:
        subprocess.run(
            ["edge-tts", "--voice", voice, "--text", text, "--write-media", mp3_path],
            check=True,
        )
        subprocess.run(["mpg123", "-q", mp3_path], check=True)
    except FileNotFoundError as e:
        print(f"[!] Required tool not found: {e}. Install edge-tts and mpg123.")
    except subprocess.CalledProcessError as e:
        print(f"[!] TTS playback failed: {e}")
    finally:
        if os.path.exists(mp3_path):
            os.remove(mp3_path)


def list_voices() -> None:
    console = Console()
    table = Table(title="Edge-TTS Voices")
    table.add_column("Lang", style="cyan")
    table.add_column("Voice", style="green")
    for lang, voice in VOICE_MAP.items():
        table.add_row(lang, voice)
    console.print(table)
