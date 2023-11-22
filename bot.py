import requests
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)
from BotDetails.handlers import start, userlar, todos

TOKEN = "6837299511:AAGFaEAKObTznuUQZs0Rulfu9MVL0_HI4p8"




updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

def register_handlers():
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text('Userlar👤'), userlar))
    
    dispatcher.add_handler(MessageHandler(Filters.text('Id orqali👤'), userlar))
    dispatcher.add_handler(MessageHandler(Filters.text('🕔Todos'),todos))

    updater.start_polling()
    updater.idle()


register_handlers()