"""Telegram bot runner"""
# encoding=utf8
import sys
import getopt
from markovify_provider import MarkovifyProvider
from dropbox_text_provider import DropboxTextProvider
from telegram_client import TelegramClient

reload(sys)
sys.setdefaultencoding('utf8')

def main():
    """Entry point"""
    auto_feed = False
    
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 't:l:n:p:d:f:a:x', ['source', 'token',
                                                            'language', 'name', 'provider', 
                                                            "dropboxtoken", "dropboxfile", "autofeed"])
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

    #If we code new providers we'll need a switch here
    text_provider = DropboxTextProvider(dropbox_access_token, dropbox_file)
    provider = MarkovifyProvider(language, text_provider)
    provider.load()
    TelegramClient(token, name, provider, auto_feed)


if __name__ == '__main__':
    main()
