import sqlite3


def get_connect_data_base(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('second.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner


@get_connect_data_base
def start(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS second_data_base(
        user_id INTEGER NOT NULL,
        money INTEGER NOT NULL DEFAULT 100,
        purchases INTEGER)''')
    conn.commit()


@get_connect_data_base
def set_values(conn, user_id: int, money: int, purchases: int = 0):
    c = conn.cursor()
    c.execute('''INSERT INTO second_data_base VALUES (?, ?, ?)''', (user_id, money, purchases))
    conn.commit()


@get_connect_data_base
def get_count_values(conn, user_id: int):
    c = conn.cursor()
    # count() - мы подсчитываем количество найденных элементов
    # По умолчанию создается столбец с названием count(user_id), что не очень удобно
    c.execute('''SELECT count(user_id) FROM second_data_base WHERE user_id = ?''', (user_id, ))
    print(c.fetchone()[0])
    # После as мы прописываем название этого столбца, так мы облегчаем дальнейшую обработку
    c.execute('''SELECT count(user_id) as count_user_id FROM second_data_base WHERE user_id = ?''', (user_id, ))
    # Остальные агрегирующие функции команды SELECT:
    # sum() - находит сумму
    # max() - находит максимальное число
    # min() - находит минимальное число
    # avr() - находит среднее арифметическое
    # Все это работает только с переменными тип INTEGER и REAL


@get_connect_data_base
def get_distinct_values(conn):
    c = conn.cursor()
    # DISTINCT - находит только уникальные значения
    c.execute('''SELECT DISTINCT user_id FROM second_data_base''')
    print(c.fetchall())


@get_connect_data_base
def get_group_values(conn):
    c = conn.cursor()
    # GROUP BY - мы группируем данные по user_id, по возрастанию
    # Затем мы сортируем данные по возрастанию, заметьте, мы сортируем столбец sum_money
    c.execute('''SELECT user_id, sum(money) as sum_money 
                 FROM second_data_base 
                 GROUP BY user_id
                 ORDER BY sum_money''')
    print(c.fetchall())


@get_connect_data_base
def delete(conn):
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS second_data_base')


if __name__ == '__main__':
    # delete()
    start()
    # set_values(user_id=2, money=15, purchases=8)
    # get_count_values(user_id=1)
    # get_distinct_values()
    get_group_values()
