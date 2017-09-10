"""AbstractBot"""
import random
import re
# encoding=utf8

class AbstractBot(object):
    """Generic bot"""

    def __init__(self, trigger_word, provider, auto_feed, meme_provider):

        #Setup class props
        self.chat_count = {}
        self.participation_frequency = 5
        self.trigger_word = trigger_word
        self.provider = provider
        self.auto_feed = auto_feed
        self.meme_provider = meme_provider

    def process_incoming_message(self, chat_id, text):
        """Incoming message handlerr"""
        regex_trigger = re.compile("(" + self.trigger_word + ")", re.IGNORECASE)

        #Reload bot
        if text == "bot reload":
            self.provider.load()
            return "Reloaded", None

        #Bot match
        elif regex_trigger.findall(text):
            self.chat_count[chat_id] = 0
            text = regex_trigger.sub('', text)
            text = self.provider.get_message(text)
            #Meme check
            meme = self.meme_provider.get_random_meme(text)

            return text, meme
        #Save new data
        else:
            chat_count_dic = self.chat_count
            if not chat_id in chat_count_dic:
                chat_count_dic[chat_id] = 0

            chat_count_dic[chat_id] = chat_count_dic[chat_id] + 1

            ##He'll join after a random number of messages between 5 and 15
            frequency = random.randint(5, 15)
            if chat_count_dic[chat_id] > frequency:
                chat_count_dic[chat_id] = 0
                text = self.provider.get_message(text)
                return text, None

            if self.auto_feed:
                self.provider.text_provider.add_text(text)
