import requests
import bs4

response = requests.get(
    f"https://nekdo.ru/censure/{page}")  # сюда get запросом вставляешь номер страницы следующей с которой парсишь, когда в бд нет новых анекдотов
page = bs4.BeautifulSoup(response.content, "html.parser")
item = page.findAll('div', 'text')
for i in item:
    print(i.get_text())
