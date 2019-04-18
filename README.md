# Chatbots
This is part of AI project try to deplay [tensor2tensor](https://github.com/tensorflow/tensor2tensor) on insert punctuations for text. To build simple environment for deploy t2t model on reality, the telegram chatbot was design as the easiest solution.

## Philosophy of design
Simplest code as mush as possible and portable.

## Quick start 
You can easy build simple program (**chatBot**) to take and send text with Telegram server through [Telgegram API](https://core.telegram.org/) and python. Then you can build model t2t to handle text retrieve by Bot.

### Get token for Bot on telegram
Before building your own chatBot on [telegram](https://telegram.org/), you need to register for your Bot. It can be finish by following some steps:
1. Open telegram, search for [@BotFather](https://telegram.me/BotFather) and start a chat
2. Type `/newbot` and following instruction 

- Go to botFather on telegram and following guide to create new chatbot
- Take token chatbot return for you and put it in Telegram_chatbot_token.txt
- Runing chatbot.py on your server
- Go to telegram and try to communicate with chat bot

## What chat bot can do ?
- Find it out in "doc"

## What you should have to build your own translate chatbot:
- Library: tensor2tensor + tensorflow matplotlib --> For training and decode AI data
- Library: python-telegram-bot --> API of telegram-bot
- Library: sh --> Running t2t as bash shell scipt wrapping on python

## Data model for running AI translator
- You should as in issue if want or read code and try to regenerate it (hint: basic following tensor2tensor introduction)

## Reference: 
- Here is my guider when I build chatbot at the first times: https://chatbotslife.com/your-first-chatbot-using-telegram-and-python-part-1-796894016ba8

### update at 2019-03-19
