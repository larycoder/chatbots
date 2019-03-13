# Get token of telegram chat bot
file = open("Telegram_chatbot_token.txt","r")
Token = file.read()

CallBot = "No"
AskBot = "No"
BotAsk = "No"
Chat_id = ""

from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from Translator import translatorAI

def main():
  # Updater update from telegram and push it to Dispatcher
  updater = Updater(Token)

  # Link updater with dispatcher
  dispatcher = updater.dispatcher
  print("Bot start")

  # Add command handle vs message handle
  start_handler = CommandHandler(['Ronet','hi'],start)
  translate_handler = CommandHandler('translate',translate)
  Message_handler = MessageHandler(Filters.text,sendMessage)

  dispatcher.add_handler(start_handler)
  dispatcher.add_handler(translate_handler)
  dispatcher.add_handler(Message_handler)

  # Start chatbot
  updater.start_polling()

  # Run the bot until you press Ctrl-C
  updater.idle()

# Handle start command
def start(bot, update):
  update.message.reply_text("Hi, I am translator bot !")
  print(update.message.chat.id)

# Handle command translate
def translate(bot,update):
  string=update.message.text[11:]
  update.message.reply_text("It may take some minutes ...")
  update.message.reply_text("Translate: \n"+translatorAI(string))

# Handler conversation with both 
def sendMessage(bot,update):
  # Define global var for state of conversation
  global AskBot, CallBot, BotAsk, Chat_id

  # put message received onto analyze
  String = update.message.text
  List = String.split(' ')

  # state 1: bot ask usr for conversation
  if CallBot == "No" and AskBot == "No" and BotAsk == "No":
    for name in List:
      if name == "@ronet20190310_bot":
        Chat_id = update.message.chat_id
        bot.sendMessage(Chat_id,"Do you call me ?")
        BotAsk = "Yes"
        return
    bot.sendMessage(Chat_id,"This conversation close")
    BotAsk = CallBot = AskBot = "No"

  # state 2: usr confirm conversation
  elif BotAsk == "Yes" and CallBot == "No" and AskBot == "No":
    for name in List:
      if name == "yes" or name == "Yes":
        bot.sendMessage(Chat_id,"What do you want ?")
        CallBot = "Yes"
        return
    bot.sendMessage(Chat_id,"This conversation close")
    BotAsk = CallBot = AskBot = "No"

  # state 3: usr ask bot for function
  elif BotAsk == "Yes" and CallBot == "Yes" and AskBot == "No":
    for name in List:
      if name == "translate" or name == "Translate":
        bot.sendMessage(Chat_id,"Enter text you want to translate !")
        AskBot = "Yes"
        return
    bot.sendMessage(Chat_id,"This feature not yet update on me, sorry\n This conversation close")   
    BotAsk = CallBot = AskBot ="No"

  # state 4: bot answer usr
  elif BotAsk == "Yes" and CallBot == "Yes" and AskBot == "Yes":
    bot.sendMessage(Chat_id,"Please waiting for translation ...")
    bot.sendMessage(Chat_id,translatorAI(String))
    bot.sendMessage(Chat_id,"This conversation close")
    BotAsk = CallBot = AskBot = "No"
  
# Main runnning function
if __name__ == '__main__':
  main()
