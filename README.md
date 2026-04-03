# Language Teacher CLI
___
![img](https://github.com/LoQiseaking69/Language-teacher-cli/blob/main/Teach.PNG)

A multilingual language teacher CLI powered by [Typer](https://typer.tiangolo.com/), [Edge-TTS](https://github.com/rany2/edge-tts), and MyMemory translation API.

## Features

- Translates English text into your chosen target language
- Speaks the translated text using realistic neural voices (Edge-TTS)
- Pinyin fallback for Mandarin Chinese
- Switchable languages and voices
- Persistent user config (`~/.language_teacher_config.json`)
- Logs translation history to `~/.language_teacher_history.jsonl`
- Lists available neural voices
- **HSK 1-3 vocabulary database** (589 words across 3 bands)
- **Typing practice** – type Chinese characters from English/pinyin prompts
- **Quiz mode** – type the English meaning for Chinese characters
- **Progress tracking** – mastery stats per word and per HSK band

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

- `language-teacher teach TEXT`  
  Translate and speak English text in the target language

- `language-teacher set LANG VOICE`  
  Set your default language and voice (e.g., `zh-CN` and `zh-CN-XiaoxiaoNeural`)

- `language-teacher list-voices`  
  Show all available voices

- `language-teacher history`  
  Show your past translated sentences

#### HSK Mandarin Commands

- `language-teacher vocab [--band 1|2|3] [--category CATEGORY] [--search QUERY]`  
  Browse HSK 1-3 vocabulary lists. Filter by band, category, or search by English/pinyin/hanzi.

- `language-teacher typing-practice [--count N] [--band 1|2|3] [--no-speak]`  
  Practice typing Chinese characters from English + pinyin prompts. Tracks your progress.

- `language-teacher quiz [--count N] [--band 1|2|3]`  
  Quiz mode: see Chinese characters and type the English meaning.

- `language-teacher progress`  
  Show your HSK vocabulary learning progress with per-band mastery stats.

- `language-teacher hsk-info`  
  Display information about available HSK bands, categories, and total word count.

## Example

```bash
# Translation workflow
language-teacher set zh-CN zh-CN-XiaoxiaoNeural
language-teacher "Where is the nearest train station?"

# HSK vocabulary practice
language-teacher hsk-info
language-teacher vocab --band 1 --category verb
language-teacher typing-practice --band 1 --count 5
language-teacher quiz --band 2 --count 10
language-teacher progress
```

## Requirements

- Python 3.8+
- `edge-tts`, `mpg123`, `typer`, `pypinyin`, `requests`, `rich`
- Linux-based system with audio output

## License

MIT
