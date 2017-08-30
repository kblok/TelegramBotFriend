"""Text provider based on Marcovify"""
import markovify
import nltk
import re

class MarkovifyProvider(object):
    """Text provider based on Marcovify"""
    def __init__(self, source_text, language):
        self.source_text = source_text
        self.load()
        self.source_text = source_text
        self.language = language

    def load(self):
        """Parses the text file in self.source_text and loads the model with markofy"""
        with open(self.source_text) as source_file:
            text = source_file.read()
            self.model = markovify.NewlineText(text)

    def add_text(self, text):
        """Add a new line in the source_text"""
        with open(self.source_text, "a") as chat_file:
            chat_file.write(text + "\n")

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