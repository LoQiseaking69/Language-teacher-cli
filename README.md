# Language Teacher CLI

A multilingual language teacher CLI powered by [Typer](https://typer.tiangolo.com/), [Edge-TTS](https://github.com/rany2/edge-tts), and MyMemory translation API.

## Features

- Translates English text into your chosen target language
- Speaks the translated text using realistic neural voices (Edge-TTS)
- Pinyin fallback for Mandarin Chinese
- Switchable languages and voices
- Persistent user config (`~/.language_teacher_config.json`)
- Logs translation history to `~/.language_teacher_history.jsonl`
- Lists available neural voices

## Installation

```bash
chmod +x install.sh
./install.sh
```

Ensure `~/.local/bin` is in your `PATH` if not already.

## Usage

```bash
language-teacher "hello world"
```

### Commands

- `language-teacher set [LANG] [VOICE]`  
  Set your default language and voice (e.g., `zh-CN` and `zh-CN-XiaoxiaoNeural`)

- `language-teacher list-voices`  
  Show all available voices

- `language-teacher history`  
  Show your past translated sentences

## Example

```bash
language-teacher set zh-CN zh-CN-XiaoxiaoNeural
language-teacher "Where is the nearest train station?"
```

## Requirements

- Python 3.7+
- `edge-tts`, `mpg123`, `typer`, `pypinyin`, `requests`, `rich`
- Linux-based system with audio output

## License

MIT
