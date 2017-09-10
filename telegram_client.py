"""Telegram Client"""
import logging
# encoding=utf8
import sys
from telegram.ext import Filters, MessageHandler, Updater

reload(sys)
sys.setdefaultencoding('utf8')

class TelegramClient(object):
    """Telegram Client"""

    def __init__(self, abstract_bot, token):

        self.abstract_bot = abstract_bot

        #Setup Login
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        #Setup Bot
        updater = Updater(token=token)
        updater.bot.abstract_bot = abstract_bot

        dispatcher = updater.dispatcher
        updater.start_polling()

        reply_handler = MessageHandler(Filters.text, self.reply)
        dispatcher.add_handler(reply_handler)
        dispatcher.add_error_handler(self.error)
        print "We're ready to go"
        updater.idle()

    @staticmethod
    def reply(bot, update):
        text, meme = bot.abstract_bot.process_incoming_message(update.message.chat_id, update.message.text)

        bot.send_message(chat_id=update.message.chat_id, text=text)
        if not meme is None:
            bot.send_photo(chat_id=update.message.chat_id, photo=meme)


    @staticmethod
    def error(bot, update, error):
        """Error handler"""
        print 'Update "%s" caused error "%s" (%s)' % (update, error, bot.name)
