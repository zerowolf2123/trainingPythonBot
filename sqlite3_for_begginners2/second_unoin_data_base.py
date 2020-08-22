import sqlite3


def get_connect_data_base(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('second_union.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner


@get_connect_data_base
def create_user1_data_base(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users1(
        user_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        tab TEXT DEFAULT tab1
    )''')
    conn.commit()


@get_connect_data_base
def create_user2_data_base(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users2(
        user_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        tab TEXT DEFAULT tab2
    )''')
    conn.commit()


@get_connect_data_base
def set_user1_values(conn, user_name: str, age: int):
    c = conn.cursor()
    c.execute('''INSERT INTO users1(user_name, age) VALUES (?, ?)''', (user_name, age))
    conn.commit()


@get_connect_data_base
def set_user2_values(conn, user_name: str, age: int):
    c = conn.cursor()
    c.execute('''INSERT INTO users2(user_name, age) VALUES (?, ?)''', (user_name, age))
    conn.commit()


@get_connect_data_base
def get_union_tabs(conn):
    c = conn.cursor()
    # UNION - объединяет 2 и больше таблицы, с учетом того, что строчки должны быть уникальны
    c.execute('''SELECT user_name, age, tab FROM users1
                 UNION SELECT user_name, age, tab FROM users2''')
    for i in c.fetchall():
        print(i)


if __name__ == '__main__':
    create_user1_data_base()
    create_user2_data_base()
    # set_user1_values(user_name='Андрей', age=38)
    # set_user2_values(user_name='Виктор', age=19)
    get_union_tabs()
