import requests
import bs4
import database


def parse_anekdot_bezmata(message):
    user = database.User.get(user_id=message.chat.id)
    user_page = user.page
    response = requests.get(
        f"https://nekdo.ru/censure/{user_page}")  # сюда get запросом вставляешь номер страницы следующей с которой парсишь, когда в бд нет новых анекдотов
    page = bs4.BeautifulSoup(response.content, "html.parser")
    item = page.findAll('div', 'text')

    for i in item:
        database.Anekdot(text=str(i.get_text())).save()

    user.cnt_likes = len(item)
    user.page = user_page + 1
    user.save()
