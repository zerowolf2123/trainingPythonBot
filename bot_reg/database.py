import sqlite3


def get_connection_base_data(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('subscribers.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner


@get_connection_base_data
def start_db(conn, force: bool = False):
    c = conn.cursor()
    if force:
        c.execute("DROP TABLE IF EXISTS subscribers")
    c.execute("""CREATE TABLE IF NOT EXISTS subscribers(
        tg_name TEXT,
        user_id INTEGER,
        full_name TEXT,
        age INTEGER,
        gender TEXT 
    )""")
    conn.commit()


@get_connection_base_data
def add_subscribers(conn, tg_name: str, user_id: int):
    c = conn.cursor()
    c.execute("SELECT user_id FROM subscribers WHERE user_id = ?", (user_id, ))
    if c.fetchone() is None:
        c.execute("INSERT INTO subscribers(tg_name, user_id) VALUES (?, ?)", (tg_name, user_id))
        conn.commit()


# В этой функции будут обновляться данные о пользователе
@get_connection_base_data
def add_subscribers_info(conn, user_id: int, full_name: str, age: int, gender: str):
    c = conn.cursor()
    c.execute("SELECT tg_name FROM subscribers WHERE user_id = ?", (user_id,))
    if c.fetchone() != None:
        # Обновляем данные в базе данных, ищем по user_id
        c.execute("UPDATE subscribers SET full_name = ? WHERE user_id = ?", (full_name, user_id))
        conn.commit()
        c.execute("UPDATE subscribers SET age = ? WHERE user_id = ?", (age, user_id))
        conn.commit()
        c.execute("UPDATE subscribers SET gender = ? WHERE user_id = ?", (gender, user_id))
        conn.commit()


# Возварщаем ники пользователей телеграмм
# Может понадобиться, если вы хотите написать пользователям от имени бота
# Можно использовать для рассылки
@get_connection_base_data
def get_subscribers_tg_names(conn):
    c, sab = conn.cursor(), []
    # * - берем все tg_name из базы данных
    for i in c.execute("SELECT * FROM subscribers ORDER BY tg_name"):
        # Обязательно берем 0 элемент, потому что по умолчанию возвращается (..., )
        sab.append(i[0])
    sab = '\n'.join(sab)
    return sab
