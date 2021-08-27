# Gelin Eguinosa Rosique

from transformers import MarianTokenizer, MarianMTModel


class Translator:
    """
    Class to translate text from a determined language to another.
    """

    # The Languages the Translation Model can work with.
    supported_languages = {
        'en', 'es', 'de', 'fr', 'it', 'ru', 'pt', 'tr', 'ar', 'oc', 'ca', 'rm',
        'wa', 'lld', 'fur', 'lij', 'lmo', 'gl', 'lad', 'an', 'mwl',
    }

    def __init__(self, text_lang, target_lang):
        """
        Initialize the Translation Model with the specified text language and
        target language.
        :param text_lang: The language of the text we received.
        :param target_lang: The language to which we are translating the text.
        """
        # Check the text and target languages are supported
        if text_lang not in self.supported_languages:
            raise Exception("The language of the Text is not supported by the"
                            " translator.")
        if target_lang not in self.supported_languages:
            raise Exception("The target language is not supported by the"
                            " translator.")

        # The name of the translation model:
        model_name = f'Helsinki-NLP/opus-mt-{text_lang}-{target_lang}'

        # Load or Download the model and tokenizer:
        self.model = MarianMTModel.from_pretrained(model_name)
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)

    def translate(self, text):
        """
        Translate a text to the target language. If text is a list of string, it
        returns a list of the translated documents.
        :param text: The text the user intends to translate.
        :return: The translated text.
        """
        # Check if we are receiving multiple texts.
        if type(text) == list:
            # Call the multiple text translation
            return self._texts_translation(text)

        # We are working with only one text
        # Translate the text
        single_translation = self._texts_translation([text])[0]
        return single_translation

    def _texts_translation(self, texts):
        """
        Translates a list of texts from their original language to the target
        language.
        :param texts: The list of texts we are going to translate.
        :return: A list with the translation of the texts.
        """
        # List were the translated texts will be stored
        translated_texts = []

        for text in texts:
            # Check if the text is too big to be translated all at once
            if len(text) > 750:
                # If the line is to big, try to split it by sentences before
                # translating
                text_sentences = text.split('.')
                # Remove all empty strings
                while '' in text_sentences:
                    text_sentences.remove('')

                # Check the text was split at least in two pieces, if we could
                # not split the text, then force the normal process.
                if len(text_sentences) > 1:
                    # If we could split the text, call this method recursively
                    translated_sentences = self._texts_translation(text_sentences)
                    big_text_translation = _rejoin_with_dots(translated_sentences)
                    translated_texts.append(big_text_translation)
                    continue

            # Translate the current text
            inputs = self.tokenizer([text], return_tensors="pt", padding=True)
            gen = self.model.generate(**inputs)
            translated_text = self.tokenizer.batch_decode(gen, skip_special_tokens=True)[0]
            # Save the translated text
            translated_texts.append(translated_text)

        return translated_texts


def _rejoin_with_dots(sentences):
    """
    Rejoin the sentences of a text that was split by dots during the
    translation because it had more than 750 characters.
    :param sentences: The sentences of the text that was split.
    :return: the rejoined text with the sentences in texts joined by dots.
    """
    # Initialize the text we are going to return with the first sentence
    text = sentences[0]

    # Iterate the sentences starting on the second one.
    for i in range(1, len(sentences)):
        # Get the sentence
        sentence = sentences[i]
        # Create the default value to the infix that will connect the
        # sentences
        infix = '.'

        # Check if we add a dot or not.
        if text[-1] == '.':
            infix = ''
        # Check if we add a space after the dot
        if text[-1] != ' ' and sentence[0] != ' ':
            infix += ' '

        text += infix + sentence

    # Add a dot at the end of the text if it doesn't have one
    if text[-1] != '.':
        text += '.'

    return text
