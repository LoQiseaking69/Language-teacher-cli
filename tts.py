import subprocess
import json
import requests
from rich.table import Table
from rich.console import Console

VOICE_MAP = {
    "zh-CN": "zh-CN-XiaoxiaoNeural",
    "zh-HK": "zh-HK-HiuGaaiNeural",
    "es-ES": "es-ES-ElviraNeural",
    "en-US": "en-US-JennyNeural",
    "fr-FR": "fr-FR-DeniseNeural"
}

def speak_text(text, voice):
    from tempfile import NamedTemporaryFile
    with NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
        mp3_path = temp_audio.name
    subprocess.run(["edge-tts", "--voice", voice, "--text", text, "--write-media", mp3_path], check=True)
    subprocess.run(["mpg123", "-q", mp3_path], check=True)
    os.remove(mp3_path)

def list_voices():
    console = Console()
    table = Table(title="Edge-TTS Voices")
    table.add_column("Lang", style="cyan")
    table.add_column("Voice", style="green")
    for lang, voice in VOICE_MAP.items():
        table.add_row(lang, voice)
    console.print(table)
