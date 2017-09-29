"""Telegram bot runner"""
# encoding=utf8
import os
import sys
import getopt
from markovify_provider import MarkovifyProvider
from dropbox_text_provider import DropboxTextProvider
from telegram_client import TelegramClient
from meme_provider import MemeProvider
from abstract_bot import AbstractBot

reload(sys)
sys.setdefaultencoding('utf8')

def main():
    """Entry point"""
    auto_feed = False
    join_every = 5
    
    #Try to get params from env
    if not os.environ.get('BOT_FRIEND_TOKEN') is None:
        token = os.environ.get('BOT_FRIEND_TOKEN')
    if not os.environ.get('BOT_FRIEND_LANGUAGE') is None:
        language = os.environ.get('BOT_FRIEND_LANGUAGE')
    if not os.environ.get('BOT_FRIEND_NAME') is None:
        name = os.environ.get('BOT_FRIEND_NAME')
    if not os.environ.get('BOT_FRIEND_DROPBOX_ACCESS_TOKEN') is None:
        dropbox_access_token = os.environ.get('BOT_FRIEND_DROPBOX_ACCESS_TOKEN')
    if not os.environ.get('BOT_FRIEND_DROPBOX_FILE') is None:
        dropbox_file = os.environ.get('BOT_FRIEND_DROPBOX_FILE')
    if not os.environ.get('BOT_FRIEND_AUTO_FEED') is None:
        auto_feed = os.environ.get('BOT_FRIEND_AUTO_FEED') == "1"
    if not os.environ.get('BOT_FRIEND_MEME_FILE') is None:
        meme_file = os.environ.get('BOT_FRIEND_MEME_FILE')
    if not os.environ.get('BOT_FRIEND_JOIN_EVERY') is None:
        join_every = os.environ.get('BOT_FRIEND_JOIN_EVERY')


    #Try to get params from arguments
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 't:l:n:d:f:a:m:e:x',
                                ['source', 'token', 'language', 'name',
                                 'dropboxtoken', 'dropboxfile', 'autofeed', 'memefile', 'joinevery'])

    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-t', '--toke'):
            token = arg
        if opt in ('-l', '--language'):
            language = arg
        if opt in ('-n', '--name'):
            name = arg
        if opt in ('-d', '--dropboxtoken'):
            dropbox_access_token = arg
        if opt in ('-f', '--dropboxfile'):
            dropbox_file = arg
        if opt in ('-a', '--autofeed'):
            auto_feed = True
        if opt in ('-m', '--memefile'):
            meme_file = arg
        if opt in ('-e', '--joinevery'):
            join_every = int(arg)


    text_provider = DropboxTextProvider(dropbox_access_token, dropbox_file)
    provider = MarkovifyProvider(language, text_provider)
    meme_text_provider = DropboxTextProvider(dropbox_access_token, meme_file)
    meme_provider = MemeProvider(meme_text_provider)
    abstract_bot = AbstractBot(name, provider, auto_feed, meme_provider, join_every)
    TelegramClient(abstract_bot, token)


if __name__ == '__main__':
    main()
