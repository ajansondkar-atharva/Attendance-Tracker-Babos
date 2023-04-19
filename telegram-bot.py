import telegram.ext
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

with open('telegram-bot.txt','r') as f:
    TOKEN = f.read()

    #update.message.reply_text("I Mr. Smarty Pants welcome you to A division!!!")
def slot_1(update,context):
    print("Demo testing...")

def message_handler(update: Update, context):
    message_text = update.message.text

    if("/" not in message_text):
        print(type(message_text))
        print(message_text)
        with open('messages.txt', 'w') as f:
            f.write(message_text)

        print("Splitting the message...")
        my_text = message_text.split()
        print("Done...")
        print("After splitting the message...")
        print(my_text)
        int_list = list(map(int, my_text))
        print("Converting to int list...")
        print(int_list)
        print("Done...")
        
updater = telegram.ext.Updater(TOKEN, use_context=True)
message_handler = MessageHandler(Filters.text, message_handler)
updater.dispatcher.add_handler(message_handler)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("1", slot_1))

updater.start_polling()
updater.idle()

