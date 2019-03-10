# Get token of telegram chat bot
file = open("Telegram_chatbot_token.txt","r")
Token = file.read()

from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from Translator import translatorAI

def main():
  # Updater update from telegram and push it to Dispatcher
  updater = Updater(Token)

  # Link updater with dispatcher
  dispatcher = updater.dispatcher
  print("Bot start")

  # Add command handle vs message handle
  start_handler = CommandHandler('Ronet', start)
  translate_handler = CommandHandler('translate',translate)

  dispatcher.add_handler(start_handler)
  dispatcher.add_handler(translate_handler)

  # Start chatbot
  updater.start_polling()

  # Run the bot until you press Ctrl-C
  updater.idle()

# Handle specific kind of update
def start(bot, update):
  update.message.reply_text("Do you call me ? please contact with my lawer first !")

# Handle text Message of update
def translate(bot,update):
  string=update.message.text[11:]
  update.message.reply_text("You absotely need to wait a long time !! please patient !!")
  update.message.reply_text("Translate: \n"+translatorAI(string))

# Main runnning function
if __name__ == '__main__':
  main()