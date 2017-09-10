"""Meme provider"""
import random

class MemeProvider(object):
    """
    It makes a list base on a tab separated file
    """
    def __init__(self, text_provider):
        text = text_provider.get_text()
        self.list = {}

        for line in text.split("\n"):
            key_val = line.split(",")

            if not key_val[0] in self.list.keys():
                self.list[key_val[0]] = []

            self.list[key_val[0]].append(key_val[1])
    

    def get_random_meme(self, text):
        """Gets a random meme based on a text"""
        matches = []

        for key, value in self.list.iteritems():
            if key in text:
                matches = matches + value

        if matches:
            return matches[random.randint(0, len(matches))]

        return None
