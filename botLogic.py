import json
import telebot
from telebot import types
import jsonOp

#str(userData[str(message.chat.id)]["currency_pair"]["BTC_USD"]["max"])

with open('config.json', 'r', encoding='utf-8') as f:
    conf = json.load(f)
with open('messages.json', 'r', encoding='utf-8') as f:
    answer = json.load(f)


bot = telebot.TeleBot(conf["bot_token"])

@bot.message_handler(commands=['start'])
def start(message):
    jsonOp.newUserId(message.chat.id)
    bot.send_message(message.chat.id, answer["start"], parse_mode='html')

@bot.message_handler(commands=['info'])
def info(message):
    with open('data.json', 'r', encoding='utf-8') as f:
        userData = json.load(f)

    markup = types.ReplyKeyboardMarkup()
    pairs = types.KeyboardButton("Пары валют")
 
    markup.add(pairs)

    bot.send_message(message.chat.id, "Что показать?", parse_mode='html', reply_markup=markup)

