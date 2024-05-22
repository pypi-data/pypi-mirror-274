from translate import Translator


class DataTranslator:
    def __init__(self, to_lang="en", from_lang="he"):
        self.translator = Translator(to_lang=to_lang, from_lang=from_lang)

    def translate_text(self, text: str) -> str:
        return self.translator.translate(text)

    def translate_data(self, data: dict) -> dict:
        translated_data = {}
        for key, value in data.items():
            translated_key = self.translate_text(key)
            translated_value = self.translate_text(value)
            translated_data[translated_key] = translated_value
        return translated_data
