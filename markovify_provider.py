"""Text provider based on Marcovify"""
import re
import markovify
import nltk

class MarkovifyProvider(object):
    """Text provider based on Marcovify"""
    def __init__(self, language, text_provider):
        self.text_provider = text_provider
        self.load()
        self.language = language

    def load(self):
        """Parses the text file in self.source_text and loads the model with markofy"""
        self.model = markovify.NewlineText(self.text_provider.get_text())

    def is_stop_word(self, word):
        """Checks whether a word is an stop word or not in the language specified in the class"""
        return word in nltk.corpus.stopwords.words(self.language)

    def get_message(self, text):
        """
        Returns a markofy text based on the text argument
        It will try to generate a message based on the words in the text
        If it's not able to do that it'll just create a random text
        """

        response = None
        regex_wrods = re.compile(r"(\w+)")
        words = regex_wrods.findall(text)
        for index in range(len(words)-1, -1, -1):
            try:
                if not self.is_stop_word(words[index]): #It should be some word
                    response = self.model.make_sentence_with_start(words[index], tries=10).lower()
                    break
            except Exception:
                pass

        if response is None:
            response = self.model.make_short_sentence(80, tries=10).lower()
        print response
        return response
