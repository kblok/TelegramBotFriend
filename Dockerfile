
FROM python:2.7-slim
LABEL Name=telegrambotfriend Version=0.0.3

ADD *.py ./
RUN pip install nltk python-telegram-bot dropbox markovify
RUN python -m nltk.downloader all

ENTRYPOINT python bot_friend.py
