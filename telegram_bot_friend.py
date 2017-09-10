"""Telegram bot runner"""
# encoding=utf8
import sys
import getopt
from markovify_provider import MarkovifyProvider
from dropbox_text_provider import DropboxTextProvider
from telegram_client import TelegramClient
from meme_provider import MemeProvider

reload(sys)
sys.setdefaultencoding('utf8')

def main():
    """Entry point"""
    auto_feed = False
    
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 't:l:n:p:d:f:a:m:x', 
            ['source', 'token', 'language', 'name', 'provider',
            'dropboxtoken', 'dropboxfile', 'autofeed', 'memefile'])

    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-t', '--toke'):
            token = arg
        if opt in ('-l', '--language'):
            language = arg
        if opt in ('-n', '--name'):
            name = arg
        if opt in ('-p', '--provider'):
            provider = arg
        if opt in ('-d', '--dropboxtoken'):
            dropbox_access_token = arg
        if opt in ('-f', '--dropboxfile'):
            dropbox_file = arg
        if opt in ('-a', '--autofeed'):
            auto_feed = True
        if opt in ('-m', '--memefile'):
            meme_file = arg

    #If we code new providers we'll need a switch here
    text_provider = DropboxTextProvider(dropbox_access_token, dropbox_file)
    provider = MarkovifyProvider(language, text_provider)
    meme_text_provider = DropboxTextProvider(dropbox_access_token, meme_file)
    meme_provider = MemeProvider(meme_text_provider)
    TelegramClient(token, name, provider, auto_feed, meme_provider)


if __name__ == '__main__':
    main()
