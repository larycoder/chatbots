# Chatbots
This is part of AI project try to deplay [tensor2tensor](https://github.com/tensorflow/tensor2tensor) on insert punctuations for text. To build simple environment for deploy t2t model on reality, the telegram chatbot was design as the easiest solution.

I following [this](https://chatbotslife.com/your-first-chatbot-using-telegram-and-python-part-1-796894016ba8) reference as a guider for first time working with telegram chatBot

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
For t2t translator model, I built simple [translator code](#translater) to retrieve text from var `string` and reply translated message.
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

### Deploy simple t2t model translator for retrieve and handle message <a name="translater"></a>
So, this is part where you can deploy your AI model on handle information and testing model. With this version, I build simple [code](https://github.com/larycoder/chatbots/blob/master/Translator.py) for working directly with [tensor2tensor](https://github.com/tensorflow/tensor2tensor)

First time working with tensor2tensor, I realize that it is complicate to wrap t2t into python code. So, I make some very cheating thing. Because when run t2t, you run directly into bash shell like:

For installing necessary lib of t2t
```
# Assumes tensorflow or tensorflow-gpu installed
pip install tensor2tensor

# Installs with tensorflow-gpu requirement
pip install tensor2tensor[tensorflow_gpu]

# Installs with tensorflow (cpu) requirement
pip install tensor2tensor[tensorflow]
```
And generate data
```
t2t-datagen \
  --data_dir=colab/data \
  --tmp_dir=colab/tmp \
  --problem=translate_envi_iwslt32k
```
Then training
```
t2t-trainer \
  --data_dir=colab/data \
  --problem=translate_envi_iwslt32k \
  --model=transformer \
  --hparams_set=transformer_base \
  --output_dir=colab/train \
  --train_steps=100000 \
  --eval_steps=100
```
And decode
```
t2t-decoder \
  --data_dir=colab/data \
  --problem=translate_envi_iwslt32k \
  --model=transformer \
  --hparams_set=transformer_base \
  --output_dir=colab/train \
  --decode_hparams="beam_size=4,alpha=0.6" \
  --decode_from_file=colab/en.txt \
  --decode_to_file=colab/translation.txt
```
As you can see, all this job can be easy to finish in bash shell and t2t model will read content from colab/en.txt then translate it into colab/translation.txt

Boom!! New idea is apper in my head that is instead of wrap t2t model into python (***VERY*** complicated) I just need to warp bash shell into python (more easier)

So now, let go deep into implementing this idea

First, you need some library to wrap bash shell (***sh***) into python and that is [sh](https://amoffat.github.io/sh/)
```
import sh
```
Now, you need to define a function to get message in
```
def translatorAI(String):
```
In this function, you will want to push string need to translate into colab/en.txt file
```
 file = open("colab/en.txt","w")
  file.write(String)
  file.close()
```
Then, you running 1 [sript.sh](https://github.com/larycoder/chatbots/blob/master/translate-script.sh) for running t2t in python as in bash shell
```
sh.sh("translate-script.sh")
```
Finally, translated string will be put in colab/translation.txt, so you need to get string from that file in return to bot. ***SIMPLE!!!***
```
file = open("colab/translation.txt","r")
  output = file.read()
  file.close()

return output
```
That is all of this small project

This is only a part of more huge project and final purpose of project is can insert punctuation to text. So we try to modify translator model of t2t to reach our target. If you have some interesting in it, feel free to see more in [here](https://github.com/linhhonblade/try-tensor2tensor/tree/master/custom_data)...





### update at 2019-04-19
