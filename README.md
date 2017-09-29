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

### Dropbox API

In order to make the bot easy to install in a docker container, the data source and the meme list file will be fetched from a Dropbox folder, so the bot and feed that file with new data and you don't have to think about the container storage.

So you will need to create a new dropbox token and set that token as an argument.

## Usage

```
python bot_friend.py -t "[telegram bot token]" -l "[language]" -n "[boot name]" -d "[dropbox token]" -f "[data source file]" -m "[meme list file]" -a [1|0]
```
 * **-t --token**: It's the Telegram token BotFather provided when the bot was created
 * **-l --language**: Language used by NLTK to detect stop words
 * **-n --name**: Trigger name. TelegramBotFriend will send a message when that name is mentioned in any message
 * **-d --dropboxtoken**: Dropbox Token where the Source file is located
 * **-f --dropboxfile**: Data source file with the chat history
 * **-m --memefile**: Comma separated file with the meme list, expressed as "trigger word,meme url"
 * **-a --autofeed**: If 1 the bot will feed the chat source with new incoming messages
 * **-e --joinevery**: Sets how many messages the bot should wait before stepping into the conversation. It will join after a random number of messages between joinevery and joinevery * 2

## Docker install

The bot can be installed in a docker container using the docker-compose.yml file as a template
