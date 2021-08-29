# Gelin Eguinosa Rosique

from language_detector import Detector
from translator import Translator


class MultiTranslator:
    """
    Class to automatically detect the language in a document and translate it
    to an specified language. Supports documents with multiple languages in
    their text.
    """
    # The Languages that the Model can work with.
    supported_languages = {
        'en', 'es', 'de', 'fr', 'it', 'ru', 'pt', 'tr', 'ar', 'oc', 'ca', 'rm',
        'wa', 'lld', 'fur', 'lij', 'lmo', 'gl', 'lad', 'an', 'mwl',
    }

    # The only languages tested with the project (to save in internet costs)
    project_languages = {'en', 'es', 'de', 'fr'}

    def __init__(self, target_lang='en'):
        """
        Initialize the internal variables and save the language that we will be
        translating to.
        :param target_lang: The language to which we are going the translate the
        documents we receive.
        """
        # --- REMOVE THIS 'IF' AFTER TESTING PHASE ---
        # Check if this is one of the languages we are using to test the
        # project, to avoid downloading another model $$$.
        if target_lang not in ['en', 'es']:
            raise Exception("The Language you are trying to use is not among"
                            " the testing languages of this project.")

        # Check if the class supports the target language.
        if target_lang not in self.supported_languages:
            raise Exception("Target language not supported.")

        # Save the Target Language.
        self.target_lang = target_lang
        # Create a Language Detector instance.
        self.lang_detector = Detector()

    def text_translation(self, text):
        """
        Detect the languages in the text and translate its content to the target
        language.
        The text can contain multiples languages. It assumes there is only one
        language per line.
        :param text: a string with the content of the document we want to
        translate.
        :return: a string with text translated to the target language.
        """
        # Separate the content of the text by lines.
        text_lines = text.split('\n')

        # Create the dictionaries where we are going to store the languages
        # and the translated content of the document.
        line_languages = {}
        line_translations = {}

        # Detect and save the languages of each of the lines
        for i in range(len(text_lines)):
            # Check that the line contains characters.
            if text_lines[i].strip() == '':
                continue
            line_languages[i] = self.lang_detector.get_language(text_lines[i])

        # Translate the documents organized by language to save time loading the
        # models.
        found_languages = set(line_languages.values())
        for lang in found_languages:
            # --- REMOVE THIS 'IF' AFTER TESTING PHASE ---
            # Check if the program detected a language outside of the ones we
            # are working with, to avoid downloading another model.
            if lang not in self.project_languages:
                continue

            # Check if the detected language is the same as the target language
            if lang == self.target_lang:
                continue

            # Create a model to translate the documents with the current
            # language.
            text_translator = Translator(lang, self.target_lang)

            # Iterate through all the lines in the text and translate the ones
            # with the current language.
            for line_id, line_lang in line_languages.items():
                if line_lang == lang:
                    translated_line = text_translator.translate(text_lines[line_id])
                    # Save the translation in a dictionary to later put back
                    # together the whole text.
                    line_translations[line_id] = translated_line

        # Put back together the translated lines of the text.
        new_text_lines = []
        for i in range(len(text_lines)):
            # Check if this line was translated
            if i in line_translations:
                new_text_lines.append(line_translations[i])
            # Add the original line when it wasn't translated
            else:
                new_text_lines.append(text_lines[i])

        # The final translated text
        translated_text = '\n'.join(new_text_lines)
        return translated_text
