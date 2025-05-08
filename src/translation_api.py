import requests
from googletrans import Translator
from bs4 import BeautifulSoup


class TranslatorBase:
    def __init__(self, word, source_lang, target_lang, max_translations=3):
        self.word = word
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.max_translations = max_translations

    def get_translations(self):
        raise NotImplementedError("Subclasses should implement this method.")


class GoogleTranslator(TranslatorBase):
    def get_translations(self):
        translator = Translator()
        translations = translator.translate(self.word, src=self.source_lang, dest=self.target_lang)
        return [translations.text]


class ReversoTranslator(TranslatorBase):
    def get_translations(self):
        url = f"https://api.reverso.net/translate/v1/translation"
        headers = {"Content-Type": "application/json"}
        params = {"from": self.source_lang, "to": self.target_lang, "text": self.word}
        response = requests.post(url, json=params, headers=headers)
        if response.status_code == 200:
            result = response.json()
            translations = result.get("translations", [])
            return [translation['text'] for translation in translations[:self.max_translations]]
        else:
            print(f"Error: {response.status_code} - Unable to fetch from Reverso. Switching to GT")
            translator = GoogleTranslator()
            translations = translator.translate(self.word, src=self.source_lang, dest=self.target_lang)
            return [translations.text]

class DeepLTranslator(TranslatorBase):
    def get_translations(self):
        url = "https://api-free.deepl.com/v2/translate"
        params = {"auth_key": "YOUR_DEEPL_API_KEY", "text": self.word, "source_lang": self.source_lang.upper(), "target_lang": self.target_lang.upper()}
        response = requests.post(url, data=params)
        if response.status_code == 200:
            result = response.json()
            return [t['text'] for t in result.get('translations', [])[:self.max_translations]]
        return [f"Error: {response.status_code} - Unable to fetch from DeepL."]


class LibreTranslate(TranslatorBase):
    def get_translations(self):
        url = "https://libretranslate.com/translate"
        params = {"q": self.word, "source": self.source_lang, "target": self.target_lang}
        response = requests.post(url, json=params)
        if response.status_code == 200:
            result = response.json()
            return [result.get("translatedText", "No translation")] 
        return [f"Error: {response.status_code} - Unable to fetch from LibreTranslate."]


class WiktionaryTranslator(TranslatorBase):
    def get_translations(self):
        try:
            url = f"https://en.wiktionary.org/w/api.php?action=query&titles={self.word}"
            response = requests.get(url)
            if response.status_code != 200:
                raise Exception(f"Error {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')
            # Find translation sections in the parsed HTML
            translation_section = soup.find(id='Translations')
            if not translation_section:
                raise Exception("No translation section found")

            # Extract translations from the list items within the section
            translations = []
            for li in translation_section.find_next('ul').find_all('li'):
                text = li.get_text(separator=" ").strip()
                translations.append(text)

            return translations if translations else ["No translations found"]
        except Exception as e:
            return [f"Error: {str(e)}"]


class TranslationService:
    @staticmethod
    def get_translator(service, word, source_lang, target_lang, max_translations=3):
        translators = {
            "google": GoogleTranslator,
            "reverso": ReversoTranslator,
            "deepl": DeepLTranslator,
            "libre": LibreTranslate,
            "wiktionary": WiktionaryTranslator
        }
        translator_class = translators.get(service)
        if translator_class:
            return translator_class(word, source_lang, target_lang, max_translations)
        raise ValueError(f"Unknown translation service: {service}")


if __name__ == "__main__":
    word = "turtle"
    source_lang = "en"
    target_lang = "de"
    service = "google"  # Change this to test different services
    translator = TranslationService.get_translator(service, word, source_lang, target_lang)
    print(f"Translations from {service.capitalize()}: {translator.get_translations()}")
