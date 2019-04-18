# Chatbots
This is part of AI project try to deplay [tensor2tensor](https://github.com/tensorflow/tensor2tensor) on insert punctuations for text. To build simple environment for deploy t2t model on reality, the telegram chatbot was design as the easiest solution.

## Philosophy of design
Simplest code as mush as possible and portable.

## Quick start 
You can easy build simple program (**chatBot**) to take and send text with Telegram server through [Telgegram API](https://core.telegram.org/) and python. Then you can build model t2t to handle text retrieve by Bot.

### Get token for Bot on telegram
Before building your own chatBot on [telegram](https://telegram.org/), you need to register for your Bot. It can be finish by following some steps:
1. Open telegram, search for [@BotFather](https://telegram.me/BotFather) and start a chat
2. Type `/newbot` and following instruction. After succeeding register, you will get your access TOKEN and [documentation](https://core.telegram.org/bots/api)
3. TOKEN is very important for accessing on your Bot, then it should be put in somewhere to using which is [Telegram_chatbot_token.txt](https://github.com/larycoder/chatbots/blob/master/Telegram_chatbot_token.txt) for my Bot. Remember ***DO NOT*** public your TOKEN.
### Setup API for telegram
[library](https://python-telegram-bot.readthedocs.io/en/stable/) provides a pure python interface for Telegram Bot API. It has some abstractions which makes the development of bots easy and straightforward. This library will take care of sending message to our API URL and get the response from that URL.
```
pip install python-telegram-bot
```
### Building program to retrieve and send message (***Bot***)
As I mention before, you will have 2 layer for the Bot and this is first part of it. You can look for whole code in [this](https://github.com/larycoder/chatbots/blob/master/chatbot.py)

First of all, you need to get token for using and store in variable as Token
```
file = open("Telegram_chatbot_token.txt","r")
Token = file.read()
```
Then import class needed to call and retrieve message from telegram which is define in sublib [telegram.ext](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.html) of [python-telegram-bot](https://python-telegram-bot.readthedocs.io/en/stable/)
```
from telegram.ext import Updater
```
<a name="dispatcherExplain"></a>
The Updater class will receive updates from Telegram and give it to dispatcher. The dispatcher has handlers attached to it which will respond appropriately depending upon whether it is a command or a normal message.

Create Updater object and send Bot token to it
```
updater = Updater(Token)
```
Link the Updater object with dispatcher then print out message that Bot ready.
```
dispatcher = updater.dispatcher
print("Bot start")
```
Define function to handle specific kind of update.
```
def start(bot, update):
  update.message.reply_text("Hi, I am translator bot !")
```
For t2t translator model, I built simple [translator code]() to retrieve text from var `string` and reply translated message.
```
from Translator import translatorAI
def translate(bot,update):
  string=update.message.text[11:]
  update.message.reply_text("It may take some minutes ...")
  update.message.reply_text("Translate: \n"+translatorAI(string))
```
There are another function handler call ***sendMessage*** in my code, but it is too complicate and unnecessary for deploying t2t model so I will not mention in here.

Now we’ll add handler to [dispatcher](#dispatcherExplain).
```
from telegram.ext import CommandHandler, MessageHandler,Filters
start_handler = CommandHandler(['Ronet','hi'],start)
translate_handler = CommandHandler('translate',translate)
Message_handler = MessageHandler(Filters.text,sendMessage)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(translate_handler)
dispatcher.add_handler(Message_handler)
```
There are a lot of handler, depending on your purpose you can choose between ***CommandHandler*** or ***MessageHandler***. CommandHandler is used for reply when ever there are some special command word after `/` is mentioned on chat/groupchat such as `/start` or `/translate`

In here, I dont mention about MessageHandler because it is unnecessary for our purpose, but you  can find out more information in [here](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.messagehandler.html)









## What you should have to build your own translate chatbot:
- Library: tensor2tensor + tensorflow matplotlib --> For training and decode AI data
- Library: python-telegram-bot --> API of telegram-bot
- Library: sh --> Running t2t as bash shell scipt wrapping on python

## Data model for running AI translator
- You should as in issue if want or read code and try to regenerate it (hint: basic following tensor2tensor introduction)

## Reference: 
- Here is my guider when I build chatbot at the first times: https://chatbotslife.com/your-first-chatbot-using-telegram-and-python-part-1-796894016ba8

### update at 2019-03-19
