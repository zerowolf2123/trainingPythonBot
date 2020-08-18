import sqlite3


def get_connection_base_data(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
            выполняет переданную функцию и закрывает за собой соединение.
            Потокобезопасно!
        """
    def inner(*args, **kwargs):
        # Создает базу данных в папке 'subscribers.db'
        # conn переменная которая взаимодействует с БД
        with sqlite3.connect('subscribers.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner


# Вместо вызова функции всегда вызывается декоратор, а в самом декораторе уже происходит вызов функции
# Можно вешать их лесенкой
# С помощью декораторов делается логирование (отлавливание ошибок)
@get_connection_base_data
def start_db(conn, force: bool = False):
    # Установка курсора, нужно для редактирования базы данных
    c = conn.cursor()
    if force:
        # В кавычках находится язык sql
        # Обнуляет таблицу если она есть
        c.execute("DROP TABLE IF EXISTS subscribers")
    # Создаем таблицу если она не существует, в скобках перечисляем название столбцов и их тип данных
    c.execute("""CREATE TABLE IF NOT EXISTS subscribers(
        tg_name TEXT,
        user_id INTEGER 
    )""")
    # Нужно указывать после каждого изменения в таблицу, чтобы сохранить их
    conn.commit()


@get_connection_base_data
def add_subscribers(conn, tg_name: str, user_id: int):
    c = conn.cursor()
    # Мы берем user_id из таблицы где user_id = user_id который мы передали
    # ? заменяется на user_id, это безопасный способ указания переменных, чтобы избежать инъекций
    # Писать именно (user_id, ), иначе sqlite3 не поймет, он глупый
    c.execute("SELECT user_id FROM subscribers WHERE user_id = ?", (user_id, ))
    # Берет первое найденное, есть еще fetchall, если вам нужно взять список данных
    if c.fetchone() != None:
        # Добавляем значения в таблицу
        c.execute("INSERT INTO subscribers(tg_name, user_id) VALUES (?, ?)", (tg_name, user_id))
        conn.commit()

