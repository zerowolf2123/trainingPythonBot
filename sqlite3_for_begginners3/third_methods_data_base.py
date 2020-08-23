import sqlite3

# Здесь мы разберем оставшиеся методы

def get_connect_data_base(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('third_methods.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner


@get_connect_data_base
def users(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_user TEXT NOT NULL,
        gender INTEGER DEFAULT 0,
        age INTEGER)''')
    conn.commit()


@get_connect_data_base
def set_users_values(conn, values: list):
    c = conn.cursor()
    # С помощью executemany мы можем сразу поместить коллекцию данных в БД, код сам все распределит
    c.executemany('''INSERT INTO users VALUES (NULL, ?, ?, ?)''', values)
    conn.commit()


@get_connect_data_base
def get_script_values(conn):
    c = conn.cursor()
    # С помощью executescript мы можем выполнить сразу несколько запросов, через ' ; '
    c.executescript('''DELETE FROM users WHERE name_user LIKE "А%";
                       UPDATE users SET age = age+1 WHERE gender = 1''')
    conn.commit()


@get_connect_data_base
def creat_script_tab(conn, values):
    c = conn.cursor()
    # BEGIN - Означает, что если какой то из запросов ниже выдаст ошибку, то сработает только создание таблицы
    c.executescript('''CREATE TABLE IF NOT EXISTS marks(
                         user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_name TEXT NOT NULL,
                         mark INTEGER NOT NULL
                   );
                   BEGIN;
                   INSERT INTO marks VALUES (NULL, "Олег", 4)''')
    conn.commit()


@get_connect_data_base
def creat_report_tab(conn, user_name, age, lesson, score):
    c = conn.cursor()
    c.executescript('''CREATE TABLE IF NOT EXISTS students(
                       user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_name TEXT NOT NULL,
                       age INTEGER
                   );
                   CREATE TABLE IF NOT EXISTS scores(
                       user_id INTEGER NOT NULL,
                       lesson TEXT NOT NULL,
                       score INTEGER
                   )''')
    conn.commit()
    c.execute('''INSERT INTO students VALUES (NULL, ?, ?)''', (user_name, age))
    conn.commit()
    # Свойство lastrowid берет id последнего запроса из таблицы, если оно есть
    user_id_stud = c.lastrowid
    c.execute('''INSERT INTO scores VALUES (?, ?, ?)''', (user_id_stud, lesson, score))
    conn.commit()


@get_connect_data_base
def get_dict_values(conn):
    # По умолчанию .fetchone, .fetchall, .fetchmany возвращает кортеж
    # conn.row_factory = sqlite3.Row - мы указываем, что возвращаемый тип данных это Словарь
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT user_name, age FROM students''')
    for i in c.fetchall():
        print(i['user_name'], i['age'])


if __name__ == '__main__':
    values = [
        ('Антон', 5),
        ('Влад', 5),
        ('Ева', 4)
    ]
    users()
    # set_users_values(values=values)
    # creat_script_tab(values=values)
    # get_script_values()
    # creat_report_tab(user_name='Оля', age=19, lesson='Информатика', score=100)
    get_dict_values()


# Как можно поместить фотографию в БД?
# binary = sqlite3.Binary(переменная с бинарными данными фотографии) - после этого мы можем поместить данные в БД как обычно

# conn.iterdump() - показывает, какие запросы нужно сделать, чтобы воссоздать базу данных и данные, которые там хранятся

