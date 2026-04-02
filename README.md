# Language Teacher CLI
___
![img](https://github.com/LoQiseaking69/Language-teacher-cli/blob/main/Teach.PNG)

A multilingual language teacher CLI powered by [Typer](https://typer.tiangolo.com/), [Edge-TTS](https://github.com/rany2/edge-tts), and MyMemory translation API.

## Features

- Translates English text into your chosen target language
- Speaks the translated text using realistic neural voices (Edge-TTS)
- **Mandarin Chinese typing drills** — practise typing characters for HSK Levels 1–3 (535 vocabulary words)
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

- `language-teacher teach [TEXT]`  
  Translate and speak English text in the target language

- `language-teacher set [LANG] [VOICE]`  
  Set your default language and voice (e.g., `zh-CN` and `zh-CN-XiaoxiaoNeural`)

- `language-teacher list-voices`  
  Show all available voices

- `language-teacher history`  
  Show your past translated sentences

- `language-teacher drill`  
  Interactive Mandarin typing practice using HSK vocabulary

- `language-teacher hsk-info`  
  Display HSK vocabulary statistics

### Typing Drill (HSK 1–3)

The `drill` command presents English words with their pinyin and asks you to type
the corresponding Chinese characters. A score summary is shown at the end.

```bash
# Practice 10 random HSK-3 words (includes levels 1–2 by default)
language-teacher drill

# Practice 20 words from HSK level 1 only
language-teacher drill --level 1 --count 20 --level-only

# Skip text-to-speech playback
language-teacher drill --no-speak
```

![Typing drill demo](https://github.com/user-attachments/assets/bc75eb31-969d-4336-8500-7eb59cc38275)

Use `language-teacher hsk-info --level 3` to see how many words are available at
each level.

## Example

```bash
language-teacher set zh-CN zh-CN-XiaoxiaoNeural
language-teacher teach "Where is the nearest train station?"
```

## Requirements

- Python 3.8+
- `edge-tts`, `mpg123`, `typer`, `pypinyin`, `requests`, `rich`
- Linux-based system with audio output

## License

MIT
