# Flask - экземпляр класса, который формирует WSGI-приложение
# render_template - нужен для компиляции html кода из .html
# url_for - Нужен для отображения url при запросах
# request - нужен для обработки запросов
# flash - нужен для отправки мнговенных сообщений при определенных действиях
# redirect - перенаправление на другой сайт, при оприделенных взаимодействиях
# session - текущая сессия
# abort - мгновенное прерывание сессии
# g - глобальная переменная во время запроса, в которую мы можем записывать любую пользовательскую информацию
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
import sqlite3
import os
from FDataBase import FDataBase

# конфигурация
# все переменные, записанные капсом, являются конфигурациями
DATABASE = '/tmp/flsite.db'
# устанавливает режим отладки
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dxdsf,v06k'
# создаем экземпляр класса
# (__name__) - мы передаем имя приложения, если все пишется в одном файле, то удобно передавать имя дериктории
app = Flask(__name__)
# загружаем всю конфигурацию
app.config.from_object(__name__)
# переопредляем путь к базе данных
# app.root_path - ссылается на текущий каталог, данного приложения
# записываем все так, чтобы придать каждой бд свою уникальность
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))
# Секретный ключ для активации сесии
# app.config['SECRET_KEY'] = 'sfdgkoeko2399s8sdhf674rkpkvsn87'

menu = [
    {'name': 'Установка', 'url': 'install-flask'},
    {'name': 'Первое приложение', 'url': 'install-file'},
    {'name': 'Обратная связь', 'url': 'contact'},
]


def connect_db():
    # подключаем базу данных
    conn = sqlite3.connect(app.config['DATABASE'])
    # меняем получаемый тип данных с кортежей, на словари
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    # Октрываем файл sql выполняем код и закрываем
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    # устанавливаем соединение, если оно не выполнено
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# teardown_appcontext срабатывает при уничтожении контекста приложения (g)
@app.teardown_appcontext
def close_db(error):
    # Закрывает соединение, если оно установлено
    if hasattr(g, 'link_db'):
        g.link_db.close()


# @app.route("/") - декоратор на обработку событий url
# ("/") - означает, что этот обработчик будет работать только с главной страницей
@app.route("/")
def index():
    # Выведет '/' - url текущей страницы
    # Нужно вводить название функции
    db = get_db()
    dbase = FDataBase(db)
    # Возвращаем текст
    return render_template('index.html', menu=dbase.getMenu())


@app.route("/about")
def about():
    return "<h1>Информация о сайте</h1>"


# Два оператора возвращают одно и то же
@app.route("/парсер")
@app.route("/parser")
def parser():
    # Всегда будет выводить '/parser' - так как ближе к названию функции
    print(url_for('parser'))
    return "<h1>Здесь будет парсер</h1>"


@app.route("/информация")
def about_html():
    # Берет файл из папки templates
    # {{ title }} - шаблонизация Jinja2
    # title - мы передаем в эту переменную наше оглавление
    return render_template('about_pars.html', title='Парсер')


@app.route("/settings")
def settings():
    return render_template('block_settings.html', title='Настройки парсера', menu=menu)


# <username> - текст, который будет браться после /profile/, обязательно в <>
# Если писать /profile/<username>/ то будет ошибка, так как это уже следующая часть url
@app.route("/profile/<username>")
# Функция принимает в себя эту переменную
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        # прерывает запрос с ошибку 404
        abort(404)
    return f'Ваш ник: {username}'


# <path:...> - нужен для того, чтобы брать весь url после /profile_new/
# Другие конверторы:
# int - для целочисленных значений
# float - для значений с плавующей точкой
@app.route("/profile_new/<path:username>")
def profile_new(username):
    return f'Ваш полный ник: {username}'


# methods=['POST'] - нужен для обработки post запросов
# Внутри можно перечислять какое угодно количество видов запросов
@app.route("/contact", methods=['POST', 'GET'])
def contact():
    # request.method - проверяет метод запроса get или post или какой то другой
    if request.method == 'POST':
        # Выводит данные, полученные с post запроса
        # Формат получаемого ответа [(<name>), (<данные>)]
        print(request.form)
        if len(request.form['username']) > 2 and len(request.form['email']) > 2:
            # Текст, который будет выводиться мгновенно
            # category - могут использоваться как расширения для классов
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    return render_template('report.html', title='Обратная связь', menu=menu)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        # Мы перенаправляем на следующую страницу, вызывая фунцию profile
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'login' and request.form['pas'] == 'password':
        # Сохраняем в сесию текущие данные, чтобы не авторизововаться в будущем
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация', menu=menu)


# @app.errorhandler(404) - обработчик ошибок
@app.errorhandler(404)
def errors(error):
    # , 404 - мы в лог выводим статус ответа
    return render_template('error.html', title='Страница не найдена', menu=menu), 404


if __name__ == '__main__':
    # Мы запускаем локальный веб сервер
    # debug=True - сайт будет указывать на все ошибки при запуске
    app.run(debug=True)

# Так мы эмулируем запрос, помогает при тестах
'''with app.test_request_context():
    print(url_for('parser'))'''


