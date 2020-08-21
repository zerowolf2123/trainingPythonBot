import sqlite3

# Типы данных которые не используются здесь:
# NULL - None в python
# REAL - вещественный тип (float в python)
# BLOB - двоичные данные

def get_connect_data_base(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('first.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res
    return inner


@get_connect_data_base
def start(conn):
    c = conn.cursor()
    # NOT NULL - означает, что name должен всега быть заполнен, по умоланию делают строку пустой
    # DEFAULT - значение по умолчанию, NOT NULL DEFAULT - задает значение по умолчанию, но запрещает этой строке быть NULL
    # PRIMARY KEY - индивидуальный ключ для каждого пользователя (1, 2, 3, ... n+1),
    # AUTOINCREMENT - автоматически прибавляет 1 к user_id
    c.execute('''CREATE TABLE IF NOT EXISTS first_data_base(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_user TEXT NOT NULL,
        gender INTEGER NOT NULL DEFAULT 1,
        age INTEGER)''')
    conn.commit()


@get_connect_data_base
def delete_table(conn):
    c = conn.cursor()
    # Удаляем таблицу если она есть
    c.execute('DROP TABLE IF EXISTS first_data_base')


@get_connect_data_base
def set_value(conn, name):
    c = conn.cursor()
    # INSERT INTO - добавляем значения в базу данных (новое значенияе)
    # Если вы указываете 'таблица'(...), вам нужно будет передать только столько аргументов, сколько переменных в скобках
    # Если вы пишете 'таблица', то передаете аргументы во все переменные КРОМЕ user_id, потому что это ключ
    # После VALUES указываем значение
    # Пишем именно (?), потому что так мы защищаем нашу базу данных от инъекций, (name, ) иначе выдаст ошибку (только когда у вас одно значение), в остальных (..., ...)
    c.execute('INSERT INTO first_data_base(name_user) VALUES (?)', (name,))
    conn.commit()


@get_connect_data_base
def set_values(conn, name, age):
    c = conn.cursor()
    c.execute('INSERT INTO first_data_base(name_user, age) VALUES (?, ?)', (name, age))
    conn.commit()


@get_connect_data_base
def get_values(conn, user_id):
    c = conn.cursor()
    # Мы берем значения name_user и age из таблице, ориентируясь по user_id
    c.execute('SELECT name_user, age FROM first_data_base WHERE user_id = ?', (user_id, ))
    # Берем первые найденные значения и возвращаем их в виде кортежа
    return c.fetchone()


@get_connect_data_base
def get_all_values(conn):
    c = conn.cursor()
    # Мы берем все данные (*) из таблицу, но при условии что age > 23
    c.execute('SELECT * FROM first_data_base WHERE age > 23')
    # fetchall() - это все найденные данные, возварщает список кортежей
    return c.fetchall()


@get_connect_data_base
def get_all_between_values(conn):
    c = conn.cursor()
    # BETWEEN 20 AND 40 означает, что мы ищем в людей, возраст которых от 20 до 40, (20<=age<=40)
    c.execute('SELECT * FROM first_data_base WHERE age BETWEEN 20 AND 40')
    return c.fetchall()
# Остальные логические операции в SQL:
# age > 20 AND gender == 0 (преоритет 2)
# age > 20 OR gender == 0 (преоритет 3)
# age IN(19, 41) - возраст может быть или 19, или 41
# age NOT IN(19, 41) - обратное значение
# NOT age = 20 - возраст не равен 20 (преоритет 1)
# Количество условий неограничено


@get_connect_data_base
def get_all_order_values(conn):
    c = conn.cursor()
    # ORDER BY - сортировка по... (по умолчанию сортирует во возрастанию)
    c.execute('SELECT * FROM first_data_base WHERE age > 20 ORDER BY age')
    print(c.fetchall())
    # Если нужно отсортировать по убыванию, то дописываем в конец DESC
    c.execute('SELECT * FROM first_data_base WHERE age > 20 ORDER BY age DESC')
    # fetchmany(limit) - мы устанавливаем лимит получаемых объктов
    print(c.fetchmany(3))
    # LIMIT - лимит выданных данных
    # OFFSET - смещение поиска данных на 1 в право, тоже само что и LIMIT 1, 2
    c.execute('SELECT * FROM first_data_base WHERE age > 20 ORDER BY age DESC LIMIT 2 OFFSET 1')
    print(c.fetchall())


@get_connect_data_base
def update_values(conn, age, name_user):
    c = conn.cursor()
    # Обновляем данные о пользователе, если нужно обновить сразу несколько данных, то перечисляйте их через запятую
    # LIKE - обращаемся к имени в базе данных, если такого имени нет, то возвращает False
    c.execute('UPDATE first_data_base SET age = ? WHERE name_user LIKE ?', (age, name_user))
    conn.commit()
    c.execute('SELECT age FROM first_data_base WHERE name_user LIKE ?', (name_user, ))
    print(c.fetchone()[0])
    # Like "..%" - значит что возраст заменится у всех, чье имя начинает с T
    # % - шаблон SQL:
    # %ин - ищет слова которые заканчиваются на 'ин'
    # %ин% - ищет слова которые содержат 'ин'
    c.execute('UPDATE first_data_base SET age = ? WHERE name_user LIKE "A%"', (age, ))
    conn.commit()
    # _ - шаблон SQL
    # T_mas - на место '_' будут подставляться все символы, он сможет найти Tomas и Tamas, если такие имена есть в БД
    c.execute('UPDATE first_data_base SET age = ? WHERE name_user LIKE "T_mas"', (age,))
    conn.commit()
    # Шаблоны можно совмещать


@get_connect_data_base
def delete_values(conn, age):
    c = conn.cursor()
    # Удаляет строки из таблицы, указывайте условия как можно точнее
    c.execute('DELETE FROM first_data_base WHERE age <= ?', (age, ))
    conn.commit()


if __name__ == '__main__':
    # delete_table()
    start()
    # set_values(name='Ivan', age=19)
    delete_values(age=18)



