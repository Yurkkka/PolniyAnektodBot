import requests
import bs4

response = requests.get(f"https://nekdo.ru/censure/")
page = bs4.BeautifulSoup(response.content, "html.parser")
item = page.findAll('div', 'text')
for i in item:
    print(i.get_text())
