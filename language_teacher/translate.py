import requests


def translate_text(text: str, target_lang: str = "zh-CN") -> str:
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": f"en|{target_lang}"}
    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
        return f"[Translation Error: {e}]"

    if response.status_code != 200:
        return "[Translation Error]"

    data = response.json()
    if data.get("responseStatus") != 200:
        return "[Translation Error]"

    translated = data["responseData"]["translatedText"]
    if translated.strip().lower() == text.strip().lower():
        print(f"[!] Warning: translation may have failed (result equals input)")
    return translated
