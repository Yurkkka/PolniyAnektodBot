import time

import telebot
from config import *
import database
from parse_anekdot import *

bot = telebot.TeleBot(token)  # access token to bot


def register_user(message):
    with database.db:
        user = database.User(cnt_likes_smatom=0, cnt_likes_bezmata=0, user_id=message.chat.id, likes="",
                             cnt_anekdots_smatom=0,
                             cnt_anekdots_bezmata=0, page_smatom=1,
                             page_bezmata=1).save()
        photo = open("images/hello.jpg", "rb")
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['start'])
def start(message):
    register_user(message)
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True)  # создание интрфейса кнопок для взаимодействия с пользователем
    markup.add(bez_mata, s_matom, likes)
    bot.send_message(message.chat.id, f"{message.chat.first_name}, добро пожаловать! Угощаю вас порцией анекдотов))",
                     reply_markup=markup)


def update_db(message, isMat):
    with database.db:
        if isMat:
            parse_anekdot_smatom(message)
        else:
            parse_anekdot_bezmata(message)


def send_anekdot_smatom(message):
    with database.db:
        user = database.User.get(user_id=message.chat.id)
        anekdot = database.AnekdotMat
        cnt_anekdots = user.cnt_anekdots_smatom
        cnt_likes = user.cnt_likes_smatom
        if cnt_anekdots == cnt_likes:
            if cnt_anekdots == 0:
                cnt_anekdots += 1
                user.save()
                flag = 1
            update_db(message, 1)
            if flag:
                user.cnt_anekdots_smatom = cnt_anekdots + 1
                user.save()
                bot.send_message(message.chat.id, f'{anekdot.get(anekdot.id == user.cnt_anekdots_smatom).text}')
                flag = 0
        else:
            user.cnt_anekdots_smatom = cnt_anekdots + 1
            user.save()
            bot.send_message(message.chat.id, f'{anekdot.get(anekdot.id == user.cnt_anekdots_smatom).text}')


def send_anekdot_bezmata(message):
    with database.db:
        user = database.User.get(user_id=message.chat.id)
        anekdot = database.AnekdotBezMata
        cnt_anekdots = user.cnt_anekdots_bezmata
        cnt_likes = user.cnt_likes_bezmata
        if cnt_anekdots == cnt_likes:
            if cnt_anekdots == 0:
                cnt_anekdots += 1
                user.save()
                flag = 1
            update_db(message, 0)
            if flag:
                user.cnt_anekdots_bezmata = cnt_anekdots + 1
                user.save()
                bot.send_message(message.chat.id, f'{anekdot.get(anekdot.id == user.cnt_anekdots_bezmata).text}')
                flag = 0
        else:
            user.cnt_anekdots_bezmata = cnt_anekdots + 1
            user.save()
            bot.send_message(message.chat.id, f'{anekdot.get(anekdot.id == user.cnt_anekdots_bezmata).text}')


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
