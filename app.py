"""
Simple Bot to reply to Telegram messages taken from the python-telegram-bot examples.
Deployed using heroku.
Author: liuhh02 https://medium.com/@liuhh02
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup,ParseMode
import os
import requests
from datetime import datetime
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5072195132:AAFD1G5nOQkAtLkddqVzIO0gpBzh2_1WTDo'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    topic_keyboard = [['/start','/get']]
    reply_markup = ReplyKeyboardMarkup(keyboard=topic_keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)
#     update.message.reply_text('Hi!')
#     help_txt = "Hey! Do you want help?"
    # bot.send_message(chat_id=update.message.chat_id, text=help_txt)
    res = "this bot is designed to fetch upcoming coding contests details, to do so click on the button 'get' given below."
    update.message.reply_text(res,reply_markup=reply_markup)
#     bot.send_message(chat_id=update.message.chat_id,text=res,reply_markup=ReplyKeyboardMarkup(keyboard=topic_keyboard,one_time_keyboard=True))



def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
   
def get(bot,update):
    contest_api_url = "https://kontests.net/api/v1/all"
    res = requests.get(contest_api_url)
    res_status = res.status_code

    if res_status == 200:
        res = res.json()
        corpus = ""
        i = 1
        for contest in res:
            if i % 10 == 0:
                bot.send_message(chat_id=update.message.chat_id,text=corpus,parse_mode=ParseMode.HTML,disable_web_page_preview=True)
                corpus = ""

            contest_name = contest["name"]
            date = contest["start_time"][:10]
            time_ = contest["start_time"][11:16]
            time_ = datetime.strptime(time_, "%H:%M").strftime("%r")
            url = contest['url']
            site = contest['site']
            text = f"#{i}: {site} - <a href='{url}'>{contest_name}</a> \n \t date - {date}, time - {time_[:5]+time_[8:]} \n"
            corpus += text
            i+=1


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("get", get))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://cont-buddy-tel-bot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
