import time

import telebot
from config import *
import database
from parse_anekdot import *

bot = telebot.TeleBot(token)  # access token to bot


def register_user(message):
    with database.db:
        user = database.User(cnt_likes=0, user_id=message.chat.id, likes="", cnt_anekdots=0, page=1).save()


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
        user = database.User
        cnt_anekdots = user.get(message.chat.id == database.User.user_id).cnt_anekdots
        cnt_likes = user.get(message.chat.id == database.User.user_id).cnt_likes
        if cnt_anekdots == cnt_likes:
            update_db(message)
        else:
            user.cnt_anekdots = cnt_anekdots + 1  # to do add save to db cnt_anekdots
            bot.send_message(message.chat.id, f'{database.Anekdot.text.get(id=cnt_anekdots)}')


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
