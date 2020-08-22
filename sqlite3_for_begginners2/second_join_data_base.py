import sqlite3

# Рассмотрим взаимодействие сразу с двумя таблицами

def get_connect_data_base(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('second_join.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner


@get_connect_data_base
def create_user_data_base(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        purchases INTEGER 
    )''')
    conn.commit()


@get_connect_data_base
def create_money_data_base(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS money(
        user_id INTEGER NOT NULL,
        money INTEGER DEFAULT 100,
        buy INTEGER DEFAULT 10
    )''')
    conn.commit()


@get_connect_data_base
def set_user_values(conn, user_name: str, age: int, purchases: int = 90):
    c = conn.cursor()
    c.execute('''INSERT INTO users(user_name, age, purchases) VALUES (?, ?, ?)''', (user_name, age, purchases))
    conn.commit()


@get_connect_data_base
def set_money_values(conn, user_id: int, money: int, buy: int = 10):
    c = conn.cursor()
    c.execute('''INSERT INTO money VALUES (?, ?, ?)''', (user_id, money, buy))
    conn.commit()


@get_connect_data_base
def get_join_values(conn):
    c = conn.cursor()
    # money.buy - мы уточняем, что берем данные именно из таблицы money
    # FROM money - мы работаем с таблицей money
    # JOIN users - подключаем как запросу таблицу users
    # ON money.user_id = users.user_id - при условии, что айди совпадают
    c.execute('''SELECT user_name, age, money.buy FROM money
                 JOIN users ON money.user_id = users.user_id''')
    for i in c.fetchall():
        print(i)
    print('\n')
    # Второй способ
    # НО если в одной из таблиц отсутсвует нужный user_id, то значения из другой таблице не будут выдаваться
    c.execute('''SELECT user_name, age, money.buy 
                 FROM users, money 
                 WHERE users.user_id == money.user_id''')
    for i in c.fetchall():
        print(i)
    print('\n')
    # LEFT JOIN - нужен для вывода ВСЕХ значений, даже если условие не выполнено
    c.execute('''SELECT user_name, age, money.buy FROM money
                     LEFT JOIN users ON money.user_id = users.user_id''')
    for i in c.fetchall():
        print(i)
    # Можно указывать несколько JOIN, если у вас больше 2 таблиц


if __name__ == '__main__':
    create_user_data_base()
    create_money_data_base()
    # set_user_values(user_name='Илья', age=19, purchases=20)
    # set_money_values(user_id=4, money=390, buy=21)
    get_join_values()
