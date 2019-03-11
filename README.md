# chatbots

## What i want to do:
- I try to build easiest chatbot on telegram depending on telegram supported API

## This chatbot should have purpose:
- Translating english to vietnamese
- Using tensor2tensor as AI translate
- Simplest code as mush as possible

## There should be 2 layers:
- AI model translation layer working with text in and return text out
- Chatbot layer wrap text into telegram

## How to build your own translate chatbot:
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

### update at 2019-03-12
