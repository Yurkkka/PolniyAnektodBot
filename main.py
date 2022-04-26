import time

import telebot
from config import *
import database
from parse_anekdot import *

bot = telebot.TeleBot(token)  # access token to bot


def register_user(message):
    with database.db:
        user = database.User(cnt_likes=0, user_id=message.chat.id, likes="", cnt_anekdots=1, page=1).save()


@bot.message_handler(commands=['start'])
def start(message):
    register_user(message)
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True)  # создание интрфейса кнопок для взаимодействия с пользователем
    markup.add(bez_mata, s_matom, likes)
    bot.send_message(message.chat.id, f"{message.chat.first_name}, добро пожаловать! Угощаю вас порцией анекдотов))",
                     reply_markup=markup)


def update_db(message):
    with database.db:
        parse_anekdot_bezmata(message)


def send_anekdot_bezmata(message):
    with database.db:
        user = database.User.get(user_id=message.chat.id)
        anekdot = database.Anekdot
        cnt_anekdots = user.cnt_anekdots
        cnt_likes = user.cnt_likes
        if cnt_anekdots == cnt_likes:
            update_db(message)
        else:
            user.cnt_anekdots = cnt_anekdots + 1
            user.save()
            bot.send_message(message.chat.id, f'{anekdot.get(anekdot.id == user.cnt_anekdots).text}')


def send_anekdot_smatom(message):
    pass


def send_likes(message):
    pass


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == bez_mata.text:
            send_anekdot_bezmata(message)
        elif message.text == s_matom.text:
            send_anekdot_smatom(message)
        elif message.text == likes.text:
            send_likes(message)


while True:  # for all time polling bot without exit from exceptions
    try:
        bot.polling(none_stop=False)
        time.sleep(0.3)
    except Exception as e:
        print(e)
        time.sleep(15)
