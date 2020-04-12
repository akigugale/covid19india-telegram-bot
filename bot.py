from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import telegram
import requests
import logging
import messages
import re
from env import getenv


def start(update: telegram.Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=messages.msg_start, parse_mode=telegram.ParseMode.HTML)

def about(update: telegram.Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=messages.msg_about, parse_mode=telegram.ParseMode.HTML)

def count(update: telegram.Update, context: CallbackContext):
    message = messages.get_count_msg()
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def today(update: telegram.Update, context: CallbackContext):
    message = messages.get_today_msg()
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def lastupdated(update: telegram.Update, context: CallbackContext):
    message = messages.get_lastupdated_msg()
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def statewise(update: telegram.Update, context: CallbackContext):
    message = messages.get_statewise_msg()
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def state(update: telegram.Update, context: CallbackContext):
    message = messages.ask_state_msg()
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML, reply_markup=telegram.ForceReply())

def handle_message(update: telegram.Update, context: CallbackContext):
    message = messages.default_msg()
    if update.message.reply_to_message:
        if update.message.reply_to_message.text == messages.ask_state_msg():
            message = messages.get_state_msg(update.message.text)

    if re.match('hi|hello|hey', update.message.text, re.IGNORECASE):
        message = messages.hello_msg(update.message.chat.first_name)

    elif re.match('.*count.*', update.message.text, re.IGNORECASE):
        message = messages.get_count_msg()

    elif re.match('.*state.*', update.message.text, re.IGNORECASE):
        state(update, context)

    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

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
    dp.add_handler(CommandHandler('state', state))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()