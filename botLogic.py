import json
import telebot
from telebot import types
import jsonOp
import threading

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
    bot.send_message(message.chat.id, "Текущие настройки: ", parse_mode='html')

@bot.message_handler(content_types=['text'])
def message(message):
    with open('data.json', 'r', encoding='utf-8') as f:
        userData = json.load(f)
    if message.chat.type == 'private':
        message_split = message.text.split()
        if message_split[0] in userData[str(message.chat.id)]["currency_pair"].keys():
            if message_split[1] == 'min':
                userData[str(message.chat.id)]["currency_pair"][message_split[0]][message_split[1]] = float(message_split[2])
                bot.send_message(message.chat.id, "Установлен минимум для " + str(message_split[0]) + " - " + 
                                str(userData[str(message.chat.id)]["currency_pair"][message_split[0]][message_split[1]]) + 
                                "", parse_mode='html')
                userData[message.chat.id]["alert_count"] = userData[message.chat.id]["alert_set"] 
            elif message_split[1] == 'max':
                userData[str(message.chat.id)]["currency_pair"][message_split[0]][message_split[1]] = float(message_split[2])
                bot.send_message(message.chat.id, "Установлен максимум для " + str(message_split[0]) + " - " + 
                                str(userData[str(message.chat.id)]["currency_pair"][message_split[0]][message_split[1]]) + 
                                "", parse_mode='html')
                userData[str(message.chat.id)]["alert_count"] = userData[str(message.chat.id)]["alert_set"] 
            else:
                bot.send_message(message.chat.id, "Я не знаю что ответить, попробуте написать /help, если забыли что делать", parse_mode='html')
        else:
            bot.send_message(message.chat.id, "Пары валют: " + message_split[0] + " нет в базе, попробуйте написать команду снова.", parse_mode='html')
        if message_split[0] == 'alert':
                userData[str(message.chat.id)]["alert_set"] = int (message_split[1])
                bot.send_message(message.chat.id, "Настройка уведомлений: будет приходить " + str(message_split[1]) + " уведомлений", parse_mode='html')
    with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(userData, f, ensure_ascii=False, indent=4)

def check_values():
    threading.Timer(1.0, check_values).start()
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('prices.json', 'r', encoding='utf-8') as f:
        price = json.load(f)
    for chat_id in data.keys():
        for pair in data[chat_id]["currency_pair"].keys():
            if data[chat_id]["currency_pair"][pair]["min"] != 0 and float(price[pair]) < data[chat_id]["currency_pair"][pair]["min"] and data[chat_id]["alert_count"] > 0:
                bot.send_message(chat_id, "Цена " + pair + " - " + str(price[pair]) +
                                " ниже минимума: " + str(data[chat_id]["currency_pair"][pair]["min"]), parse_mode='html')
                data[chat_id]["alert_count"] -= 1
            elif data[chat_id]["currency_pair"][pair]["max"] != 0 and float(price[pair]) > data[chat_id]["currency_pair"][pair]["max"]  and data[chat_id]["alert_count"] > 0:
                bot.send_message(chat_id, "Цена " + pair + " - " + str(price[pair]) +
                                " больше максимума : " + str(data[chat_id]["currency_pair"][pair]["max"]), parse_mode='html')
                data[chat_id]["alert_count"] -= 1
    with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4) 
