from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import telegram
import requests
import logging
import messages
import re
import json
from datetime import time
from env import getenv

def get_users():
    try:
        with open('users.json') as f:
            data = json.load(f)
            return data
    except Exception as e:
        if type(e).__name__ == 'JSONDecodeError' or type(e).__name__ == 'FileNotFoundError':
            open('users.json', 'w+').write(json.dumps({}))
            return {}
        else:
            logging.error("Exception occured", exc_info=True)
    return False

def save_users(users):
    try:
        open("users.json", "w").write(json.dumps(users))
    except Exception:
        logging.error("Exception occured", exc_info=True)

def add_user(chat_id, username, first_name):
    users = get_users()
    user_data = {
        "username": username,
        "first_name": first_name,
    }
    users[str(chat_id)] = user_data
    save_users(users)

def start(update: telegram.Update, context: CallbackContext):
    chat_id = update.message.chat_id

    add_user(chat_id, update.message.chat.username, update.message.chat.first_name)

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

def districtwise(update: telegram.Update, context: CallbackContext):
    message = messages.ask_state_for_districtwise_msg()
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML, reply_markup=telegram.ForceReply())

def daily_message(context: CallbackContext):
    users = get_users()
    message = messages.get_count_msg()
    for chat_id in users:
        try:
            context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)
        except Exception as e:
            if type(e).__name__ == 'Unauthorized':
                print('{name} has blocked the bot.'.format(name=users[chat_id]['first_name']))
            continue

def subscribe(update: telegram.Update, context: CallbackContext):
    chat_id = update.message.chat_id

    add_user(chat_id, update.message.chat.username, update.message.chat.first_name)

    message = messages.subscription_success()
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

def unsubscribe(update: telegram.Update, context: CallbackContext):
    chat_id = update.message.chat_id

    users = get_users()
    del users[str(chat_id)]
    save_users(users)

    message = messages.unsubscription_success()
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)


def handle_message(update: telegram.Update, context: CallbackContext):
    message = messages.default_msg()
    if update.message.reply_to_message:
        if update.message.reply_to_message.text == messages.ask_state_msg():
            message = messages.get_state_msg(update.message.text)
        if update.message.reply_to_message.text == messages.ask_state_for_districtwise_msg():
            message = messages.get_district_msg(update.message.text)

    if re.match('hi|hello|hey', update.message.text, re.IGNORECASE):
        message = messages.hello_msg(update.message.chat.first_name)

    elif re.match('.*count', update.message.text, re.IGNORECASE):
        message = messages.get_count_msg()

    elif re.match('.*state', update.message.text, re.IGNORECASE):
        state(update, context)

    elif re.match('.*unsubscribe', update.message.text, re.IGNORECASE):
        unsubscribe(update, context)

    elif re.match('.*subscribe', update.message.text, re.IGNORECASE):
        subscribe(update, context)

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
    dp.add_handler(CommandHandler('districtwise', districtwise))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.job_queue.run_daily(
        daily_message,
        time(hour=17, minute=22),
        name='daily_count',
        days=(0, 1, 2, 3, 4, 5, 6),
    )

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
