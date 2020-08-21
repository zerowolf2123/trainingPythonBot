import sqlite3


# Данный способ открытия и закрытия таблицы не является надежным
def start_1():
    # Мы подключаемся (если нет то создаем) к базе данных
    # Файл с бд должен находится в том же каталоге что и исполняемый код
    conn = sqlite3.connect('learn.db')
    # Возвращется экземпляр класса Cursor, нужен для дальнейшей работы с бд
    c = conn.cursor()
    # execute(...) нужен для работы с бд уже на прямую
    # Язык SQL нужно писать капсом, но sqlite3 поймет и строчное написание
    # Здесь мы создаем таблицу ЕСЛИ ее еще нет в (...) через запятаю прописываем название колонок
    c.execute("""CREATE TABLE IF NOT EXISTS my_data_base(
        name TEXT, 
        age INTEGER 
    )""") # TEXT - все равно что str, INTEGER - int в python
    # Нужно указывать после каждого изменения в таблицу, чтобы сохранить их
    conn.commit()
    # Прерываем соединение с базой данных (ОБЯЗАТЕЛЬНО), в случае ошибки база данных не закрывается
    conn.close()


# Безопасный способ открыти и закрытия базы данных
def start_2():
    # Работаем с базой данных через контекст менеджера, автоматически закрывает таблицу, даже в случае ошибки
    with sqlite3.connect('learn.db') as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS my_data_base(
            name TEXT, 
            age INTEGER 
        )""")
        # Нужно указывать после каждого изменения в таблицу, чтобы сохранить их
        conn.commit()


# Самый удобный и оптимизированный способ открытия и закрытия бд, навешивая start_3 как декоратор
# func принимает функцию, которую мы вызвали
def start_3(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
            выполняет переданную функцию и закрывает за собой соединение.
            Потокобезопасно!
        """
    def inner(*args, **kwargs):
        # Создает базу данных в папке 'subscribers.db'
        # conn переменная которая взаимодействует с БД
        with sqlite3.connect('subscribers.db') as conn:
            kwargs['conn'] = conn
            # Запускает функцию, которая нам нужна и передает в нее conn
            res = func(*args, **kwargs)
        return res
    return inner


# Дальше работаем только с start_3
# Всегда сначала запускается функцию декоратор
@start_3
def create_tab(conn):
    c = conn.cursor()

