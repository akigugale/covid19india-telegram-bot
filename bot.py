from telegram.ext import *
import telegram
from telegram import *
import requests
import logging
import messages
import json


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

def coronaupdates1(update, context):
    api = "https://pomber.github.io/covid19/timeseries.json"
    api = json.loads(requests.get(api).content)
    reply_keyboard = []
    for i in api:
        reply_keyboard.append(i)
    reply_keyboard.sort()
    for i in range(len(reply_keyboard)):
        reply_keyboard[i] = [reply_keyboard[i]]
    update.message.reply_text("Please select a country name:", reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True, selective=True))
    return 0


def coronaupdates2(update, context):
    global country
    country = update.message.text
    api = "https://pomber.github.io/covid19/timeseries.json"
    api = json.loads(requests.get(api).content)
    if country in api:
        reply_keyboard = []
        for i in api[country]:
            reply_keyboard.append([i['date']])
        reply_keyboard = reply_keyboard[::-1]
        update.message.reply_text("Please select a date:", reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True, selective=True))
        return 1
    else:
        text = "You have selected an invalid option!"
        update.message.reply_text(text)
        return ConversationHandler.END


def coronaupdates3(update, context):
    api = "https://pomber.github.io/covid19/timeseries.json"
    api = json.loads(requests.get(api).content)
    date = update.message.text
    for i in api[country]:
        if i["date"] == date:
            url = i
            break
    if url:
        text = f'Cases: {url["confirmed"]}\n'
        text += f'Deaths: {url["deaths"]}\n'
        text += f'Recovered: {url["recovered"]}'
    else:
        text = "You have selected an invalid option!"
    update.message.reply_text(text)
    return ConversationHandler.END


def wrongOption(update, context):
    text = "You have selected an invalid option!"
    update.message.reply_text(text)
    return ConversationHandler.END




def main():
    updater = Updater('API KEY', use_context=True)
    dp = updater.dispatcher
    logging.basicConfig(filename='bot.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',start))
    dp.add_handler(CommandHandler('count',count))
    dp.add_handler(CommandHandler('today',today))
    dp.add_handler(CommandHandler('statewise',statewise))
    dp.add_handler(CommandHandler('about',about))
    dp.add_handler(CommandHandler('lastupdated',lastupdated))
    corona_states = {0: [MessageHandler(Filters.all, coronaupdates2)], 1: [
        MessageHandler(Filters.text, coronaupdates3)]}
    corona_handler = ConversationHandler(entry_points=[CommandHandler(
        'coronavirus', coronaupdates1)], states=corona_states, fallbacks=[MessageHandler(Filters.all, wrongOption)])
    dp.add_handler(corona_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
