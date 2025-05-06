import requests

def translate_text(text, target_lang="zh-CN"):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": f"en|{target_lang}"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["responseData"]["translatedText"]
    return "[Translation Error]"
