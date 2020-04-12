from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import requests
import logging
import messages
from env import getenv


def start(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=messages.msg_start, parse_mode=telegram.ParseMode.HTML)

def about(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=messages.msg_about, parse_mode=telegram.ParseMode.HTML)

def count(bot, update):
    message = messages.get_count_msg()
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def today(bot, update):
    message = messages.get_today_msg()
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def lastupdated(bot, update):
    message = messages.get_lastupdated_msg()
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def statewise(bot, update):
    message = messages.get_statewise_msg()
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def handle_message(bot, update):
    message = 'Hi'
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def main():
    updater = Updater(getenv('API_KEY'), use_context=True)
    dp = updater.dispatcher
    logging.basicConfig(filename='bot.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',start))
    dp.add_handler(CommandHandler('count',count))
    dp.add_handler(CommandHandler('today',today))
    dp.add_handler(CommandHandler('statewise',statewise))
    dp.add_handler(CommandHandler('about',about))
    dp.add_handler(CommandHandler('lastupdated',lastupdated))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()