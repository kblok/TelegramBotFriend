"""Telegram bot runner"""
import logging
import random
import re
# encoding=utf8
import sys

import markovify
import nltk
from telegram.ext import Filters, MessageHandler, Updater
import getopt

reload(sys)
sys.setdefaultencoding('utf8')

class TelegramBotFriend(object):
    """Telegram Bot Runner"""

    def __init__(self, source_text, token, language, trigger_word):

        #Setup class props
        self.source_text = source_text
        self.load_model()
        self.chat_count = {}
        self.participation_frequency = 5
        self.source_text = source_text
        self.language = language
        self.trigger_word = trigger_word

        #Setup Login
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        #Setup Bot
        updater = Updater(token=token)
        updater.bot.bot_friend = self

        dispatcher = updater.dispatcher
        updater.start_polling()

        reply_handler = MessageHandler(Filters.text, self.reply)
        dispatcher.add_handler(reply_handler)
        dispatcher.add_error_handler(self.error)
        print "We're ready to go"
        updater.idle()

    def load_model(self):
        """Parses the text file in self.source_text and loads the model with markofy"""
        with open(self.source_text) as source_file:
            text = source_file.read()
            self.model = markovify.NewlineText(text)

    def add_text_to_model(self, text):
        """Add a new line in the source_text"""
        with open(self.source_text) as chat_file:
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

    @staticmethod
    def reply(bot, update):
        """Telegram message handler"""
        regex_trigger = re.compile("(" + bot.bot_friend.trigger_word + ")", re.IGNORECASE)
        text = update.message.text

        #Reload bot
        if text == "Bot reload":
            bot.send_message(chat_id=update.message.chat_id, text="Reloading")
            bot.bot_friend.load_model()
            bot.send_message(chat_id=update.message.chat_id, text="Reloaded")

        #Bot match
        elif regex_trigger.findall(text):
            bot.bot_friend.chat_count[update.message.chat_id] = 0
            text = regex_trigger.sub('', text)
            text = bot.bot_friend.get_message(text)
            bot.send_message(chat_id=update.message.chat_id, text=text)

        #Save new data
        else:
            chat_count_dic = bot.bot_friend.chat_count
            if not update.message.chat_id in chat_count_dic:
                chat_count_dic[update.message.chat_id] = 0

            chat_count_dic[update.message.chat_id] = chat_count_dic[update.message.chat_id] + 1

            ##He'll join after a random number of messages between 5 and 15
            frequency = random.randint(5, 15)
            if chat_count_dic[update.message.chat_id] > frequency:
                chat_count_dic[update.message.chat_id] = 0
                text = bot.bot_friend.get_message(text)
                bot.send_message(chat_id=update.message.chat_id, text=text)

            bot.bot_friend.add_text_to_model(update.message.text)


    @staticmethod
    def error(bot, update, error):
        """Error handler"""
        print 'Update "%s" caused error "%s" (%s)' % (update, error, bot.name)


def main():
    """Entry point"""

    try:
        opts, _ = getopt.getopt(sys.argv[1:], 's:t:l:n', ['source', 'token',
                                                            'langauge', 'name'])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-s', '--source'):
            source = arg
        if opt in ('-t', '--toke'):
            token = arg
        if opt in ('-l', '--language'):
            language = arg
        if opt in ('-n', '--name'):
            name = arg

    TelegramBotFriend(source, token, language, name)


if __name__ == '__main__':
    main()
