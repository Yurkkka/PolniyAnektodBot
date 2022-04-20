import time

import telebot
from config import *

bot = telebot.TeleBot(token)  # access token to bot


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True)  # создание интрфейса кнопок для взаимодействия с пользователем
    markup.add(bez_mata, s_matom, likes)
    bot.send_message(message.chat.id, f"{message.chat.first_name}, добро пожаловать! Угощаю вас порцией анекдотов))",
                     reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    pass


while True:  # for all time polling bot without exit from exceptions
    try:
        bot.polling(none_stop=False)
        time.sleep(0.3)
    except Exception as e:
        print(e)
        time.sleep(15)
