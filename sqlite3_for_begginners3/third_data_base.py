import sqlite3


def get_connect_data_base(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('third.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner


@get_connect_data_base
def users(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER NOT NULL,
        name_user TEXT NOT NULL,
        gender INTEGER DEFAULT 0,
        age INTEGER)''')
    conn.commit()


@get_connect_data_base
def marks(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS marks(
            user_id INTEGER NOT NULL,
            lesson TEXT NOT NULL,
            mark INTEGER NOT NULL)''')
    conn.commit()


@get_connect_data_base
def set_users_values(conn, user_id: int, name_user: str, age: int, gender: int = 0):
    c = conn.cursor()
    c.execute('''INSERT INTO users(user_id, name_user, gender, age) VALUES (?, ?, ?, ?)''', (user_id, name_user, gender, age))
    conn.commit()


@get_connect_data_base
def set_marks_values(conn, user_id: int, lesson: str, mark: int):
    c = conn.cursor()
    c.execute('''INSERT INTO marks(user_id, lesson, mark) VALUES (?, ?, ?)''', (user_id, lesson, mark))
    conn.commit()


@get_connect_data_base
def get_values(conn):
    c = conn.cursor()
    # В (...) находится вложенный запрос, он выполняется в первую очередь
    # В случае логической операции, всегда берется первый найденный результат, если вложенный запрос возвращает сразу несколько значений
    c.execute('''SELECT users.name_user, marks.lesson, marks.mark FROM marks
                 JOIN users ON marks.user_id = users.user_id
                 WHERE marks.mark > (
                 SELECT mark FROM marks WHERE user_id = 2 AND lesson LIKE "Информатика"
                 ) AND marks.lesson LIKE "Информатика"''')
    for i in c.fetchall():
        print(i)
    # Вложенные запросы могут быть у SELECT, INSERT, UPDATE и DELETE
    # Глубины вложенности нет
    # Не рекомендуется использовать, только в крайнем случае


@get_connect_data_base
def delete(conn):
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('DROP TABLE IF EXISTS marks')


if __name__ == '__main__':
    # delete()
    users()
    marks()
    # set_users_values(user_id=3, name_user='Егор', age=21, gender=0)
    # set_marks_values(user_id=3, lesson='Информатика', mark=5)
    get_values()
