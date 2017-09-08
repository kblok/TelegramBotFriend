"""DropboxTextProvider is responsible for loading and saving a text file from dropbox"""
import os
import datetime
import time
import dropbox
from dropbox.files import WriteMode

class DropboxTextProvider(object):
    def __init__(self, access_token, text_path):
        self.text_path = text_path
        self.local_path = "." + text_path
        self.dropbox_client = dropbox.Dropbox(access_token)

    def get_text(self):
        """Gets the text file and returns its content"""
        self.dropbox_client.files_download_to_file(self.local_path, self.text_path, None)
        with open(self.local_path, "r") as chat_file:
            return chat_file.read()

    def add_text(self, text):
        """Adds the line to the existing file and uploads it to Dropbox"""
        with open(self.local_path, "a") as chat_file:
            chat_file.write(text + "\n")
        with open(self.local_path, "r") as chat_file:
            self.dropbox_client.files_upload(chat_file.read(), self.text_path, mode=WriteMode('overwrite'))
