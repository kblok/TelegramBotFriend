# TelegramBotFriend
Telegram Bot based on Markovify

## Prerequisites

### Setup Telegram bot.
You need to setup a bot in Telegram. You can follow [this tutorial](https://core.telegram.org/bots#6-botfather) and make sure that Privacy mode is disabled you can read more about it [here](https://core.telegram.org/bots#privacy-mode)

### Download NLTK in your language

TelegramBotFriend uses [nltk](https://github.com/nltk/nltk) in order to detect stop words. Follow [nltk instructions](http://www.nltk.org/data.html) to download the stop words for the language you're going to use.

### The most important piece: Content

You can download your chat history using [this extension](https://chrome.google.com/webstore/detail/save-telegram-chat-histor/kgldnbjoeinkkgpphaaljlfhfdbndfjc). You could use any other source, e.g. you could download this [Die Hard script](http://www.imsdb.com/scripts/Die-Hard.html) and invite Bruce Willis to your group.

After picking your source text you might need to process it, e.g. You might need to remove urls from your history, or special characters.

## Usage

```
python telegram_bot_friend.py  -s "[your history file name]" -t "[telegram bot token]" -l "[language]" -n "[boot name]"
```
 * **-s --source**: Chat history path
 * **-t --token**: It's the Telegram token BotFather provided when the bot was created
 * **-l --language**: Language used by NLTK to detect stop words
 * **-n --name**: Trigger name. TelegramBotFriend will send a message when that name is mentioned in any message
 
 
 
