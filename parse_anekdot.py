import requests
import bs4
import database


def parse_anekdot_smatom(message):
    user = database.User.get(user_id=message.chat.id)
    anekdot = database.AnekdotMat
    user_page = user.page_smatom
    response = requests.get(
        f"https://nekdo.ru/censure/{user_page}")  # сюда get запросом вставляешь номер страницы следующей с которой парсишь, когда в бд нет новых анекдотов
    page = bs4.BeautifulSoup(response.content, "html.parser")
    item = page.findAll('div', 'text')

    for i in item:
        anekdot.create(text=str(i.get_text()))

    user.cnt_likes_smatom = len(item)
    user.page_smatom = user_page + 1
    user.save()


def parse_anekdot_bezmata(message):
    user = database.User.get(user_id=message.chat.id)
    anekdot = database.AnekdotBezMata
    user_page = user.page_bezmata
    response = requests.get(
        f"https://nekdo.ru/old/{user_page}")  # сюда get запросом вставляешь номер страницы следующей с которой парсишь, когда в бд нет новых анекдотов
    page = bs4.BeautifulSoup(response.content, "html.parser")
    item = page.findAll('div', 'text')

    for i in item:
        anekdot.create(text=str(i.get_text()))

    user.cnt_likes_bezmata = len(item)
    user.page_bezmata = user_page + 1
    user.save()
