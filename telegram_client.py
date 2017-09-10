"""Telegram Client"""
import os
import logging
import random
import re
# encoding=utf8
import sys
from telegram.ext import Filters, MessageHandler, Updater
import nltk

reload(sys)
sys.setdefaultencoding('utf8')

class TelegramClient(object):
    """Telegram Client"""

    def __init__(self, token, trigger_word, provider, auto_feed, meme_provider):

        #Setup class props
        self.chat_count = {}
        self.participation_frequency = 5
        self.trigger_word = trigger_word
        self.provider = provider
        self.auto_feed = auto_feed
        self.meme_provider = meme_provider

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

    @staticmethod
    def reply(bot, update):
        """Telegram message handler"""
        regex_trigger = re.compile("(" + bot.bot_friend.trigger_word + ")", re.IGNORECASE)
        text = update.message.text

        #Reload bot
        if text == "bot reload":
            bot.send_message(chat_id=update.message.chat_id, text="Reloading")
            bot.bot_friend.provider.load()
            bot.send_message(chat_id=update.message.chat_id, text="Reloaded")

        #Bot match
        elif regex_trigger.findall(text):
            bot.bot_friend.chat_count[update.message.chat_id] = 0
            text = regex_trigger.sub('', text)
            text = bot.bot_friend.provider.get_message(text)
            bot.send_message(chat_id=update.message.chat_id, text=text)

            #Meme check
            meme = bot.bot_friend.meme_provider.get_random_meme(text)
            if not meme is None:
                bot.send_photo(chat_id=update.message.chat_id, photo=meme)

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
                text = bot.bot_friend.provider.get_message(text)
                bot.send_message(chat_id=update.message.chat_id, text=text)

            if bot.bot_friend.auto_feed:
                bot.bot_friend.provider.text_provider.add_text(update.message.text)


    @staticmethod
    def error(bot, update, error):
        """Error handler"""
        print 'Update "%s" caused error "%s" (%s)' % (update, error, bot.name)