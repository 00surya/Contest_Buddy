from flask import Flask,request
from telegram.ext import Updater, InlineQueryHandler,MessageHandler, CommandHandler,Filters,Dispatcher
from telegram import Bot,Update,ReplyKeyboardMarkup,ParseMode
import requests
from datetime import datetime

contest_api_url = "https://kontests.net/api/v1/all"


topic_keyboard = [
    ['/start','/get'],
    # ['technology','science','entertainment'],
    # ['health','sports']
]   
TOKEN = '5072195132:AAFD1G5nOQkAtLkddqVzIO0gpBzh2_1WTDo'
app = Flask(__name__)

@app.route('/')
def ok():
    return "ok"    

@app.route("/favicon.ico")
def favicon():
    return "", 200

@app.route('/'+TOKEN,methods = ['GET','POST'])
def webhook():
    """ webhook view which recives updates from telegram"""
    update = Update.de_json(request.get_json(force=True),bot)
    dp.process_update(update)
    return "test pass...."    


def start(bot,update):
    print("hello")
    help_txt = "Hey! Do you want help?"
    # bot.send_message(chat_id=update.message.chat_id, text=help_txt)
    res = "this bot is designed to fetch upcoming coding contests details, to do so click on the button 'get' given below."
    bot.send_message(chat_id=update.message.chat_id,text=res,reply_markup=ReplyKeyboardMarkup(keyboard=topic_keyboard,one_time_keyboard=True))

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


import os
if __name__ == "__main__":
    global bot
    bot = Bot(TOKEN)
    bot.set_webhook(f"https://cont-buddy-tel-bot.herokuapp.com/{Token}")
    dp = Dispatcher(bot,None)
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('get',get))
    app.run(debug=True)















# res = requests.get(contest_api_url)
# res_status = res.status_code
# if res_status == 200:
#     res = res.json()
#     for contest in res:
#         print(contest)
