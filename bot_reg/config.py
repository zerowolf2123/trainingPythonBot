TG_TOKEN = '1344744:AExu7x9Atuk_FQe0IozXMDalzVT8kwY'


# Проверяет, чтобы введенный возраст был числом и чтобы пользователю не было 50000 или -2314 лет
def valid_age(text: str):
    try:
        age = int(text)
    except:
        return None
    if 6 <= age <= 100:
        return age
