import json
import os
from typing import Any, Dict

CONFIG_PATH = os.path.expanduser("~/.language_teacher_config.json")
ALLOWED_KEYS = {"language", "voice"}


def load_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
        return {k: v for k, v in data.items() if k in ALLOWED_KEYS}
    except (json.JSONDecodeError, OSError):
        return {}


def save_config(cfg: Dict[str, Any]) -> None:
    clean = {k: v for k, v in cfg.items() if k in ALLOWED_KEYS}
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(clean, f, indent=2)
    except OSError as e:
        print(f"[!] Could not save config: {e}")
