import sys
import urllib.request
import urllib.parse
import json

# Offline fallback dictionary for demonstration
TRANSLATIONS = {
    "hello": {"es": "hola", "fr": "bonjour", "de": "hallo", "it": "ciao"},
    "how are you": {"es": "¿cómo estás?", "fr": "comment ça va?", "de": "wie geht es dir?", "it": "come stai?"},
    "thank you": {"es": "gracias", "fr": "merci", "de": "danke", "it": "grazie"},
    "goodbye": {"es": "adiós", "fr": "au revoir", "de": "auf wiedersehen", "it": "arrivederci"}
}

def translate_offline(text, target_lang):
    text_clean = text.lower().strip()
    if text_clean in TRANSLATIONS:
        return TRANSLATIONS[text_clean].get(target_lang, None)
    return None

def translate_online(text, target_lang):
    # Free public translation API (MyMemory API)
    url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair=en|{target_lang}"
    req = urllib.request.Request(url, headers={"User-Agent": "Antigravity-Agent"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data.get("responseData"):
                return data["responseData"]["translatedText"]
    except Exception:
        pass
    return None

def main():
    print("--- Translatify AI CLI ---")
    print("Supports English to: es (Spanish), fr (French), de (German), it (Italian)")
    print("-" * 40)
    
    while True:
        text = input("Enter English text to translate (or 'exit'): ").strip()
        if text.lower() == 'exit':
            sys.exit(0)
            
        target = input("Enter target language code (es/fr/de/it): ").strip().lower()
        if target not in ["es", "fr", "de", "it"]:
            print("Unsupported language code.
")
            continue
            
        # Try offline dictionary first
        translated = translate_offline(text, target)
        source_mode = "Offline Dictionary"
        
        # Fallback to online translation API
        if not translated:
            print("Connecting to translation API...")
            translated = translate_online(text, target)
            source_mode = "MyMemory Translation API"
            
        if translated:
            print(f"
Translation ({source_mode}):")
            print(f" Original  : {text}")
            print(f" Translated: {translated}
")
        else:
            print("Translation failed. Check network connection.
")

if __name__ == "__main__":
    main()
