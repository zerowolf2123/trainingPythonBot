import requests
from bs4 import BeautifulSoup
import csv

# Это стартовая страница сайта, который мы будем парсить
# Нужно для того, чтобы конкотенировать запросы
HOST = 'https://auto.ru/'
# Страница которую мы будем парсить
URL = 'https://auto.ru/balashiha/cars/jeep/all/'
# Эти два заголовка нам нужны для того, чтобы сайт думал, что мы реальные пользователи
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}
FILE = 'cars_ru.csv'


# Мы передаем наш URL и параметры запроса
def get_html(url, params=None):
    # requests.get - Мы посылаем GET запрос на страницу и сохраняем ответ в html
    # params - это параметры запроса
    html = requests.get(url=url,
                        params=params,
                        headers=HEADERS)
    return html


def get_contents(html):
    # BeautifulSoup нужен для самой работы с кодом сайта
    # html.text - мы передаем ТЕКСТ ответа, сам код
    # 'html.parser' - указываем, каким парсером мы будем пользоваться (лучше всего lxml)
    soup = BeautifulSoup(html.text, 'html.parser')
    # .find_all(описание) - ищем все элементы кода, который подходят под описание
    contents = soup.find_all('div', class_='ListingItem-module__container')
    content = []
    for value in contents:
        # ВАЖНО!! Мы работаем дальше с элементами страницу, которые находятся внутри <div class='ListingItem-module__container'>...</div>
        content.append({
            # Необязательно указывать весь путь к тексту, главное чтобы конечный запрос был уникальным
            # get_tex(strip=True) - берем текст и убираем все лишние пробелы и '\n'
            'title': value.find('a', class_='ListingItemTitle-module__link').get_text(strip=True),
            # .get('href') - мы берем содержимое из href=...
            'url': value.find('a', class_='ListingItemTitle-module__link').get('href'),
            'image': value.find('a', class_='ListingItemThumb').get('href'),
        })
    return content


def save_csv(content, file):
    # Открываем файл, если его не то создаем
    # 'w' - открываем на запись
    with open(file, 'w', newline='') as f:
        # Подключаем файл к работе
        writer = csv.writer(f, delimiter=';')
        # Создаем столбцы
        writer.writerow(['Название машины', 'Ссылка на продукт', 'Фотография'])
        for i in content:
            writer.writerow([
                i['title'],
                i['url'],
                i['image']
            ])


if __name__ == '__main__':
    html = get_html(URL)
    # .ok - мы проверяем запрос на валидность
    # Если результат 200 <= x < 400 - то запрос удачный
    if html.ok:
        cars = []
        # Если вы хотите добавлять данны в csv файл, то обязательно используйте .extend()
        cars.extend(get_contents(html))
        save_csv(cars, FILE)
    else:
        print('Error')

# Сохранение в csv может выдавать ошибку из за запрещенных символов при парсинге