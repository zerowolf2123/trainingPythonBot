from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from bot_with_sql.config import TG_TOKEN
from bot_with_sql.data_sqlite3 import start_db, add_subscribers


# CallbackContext нужен для работы с объектами Bot
def do_start(update: Update, context: CallbackContext):
    user = update.effective_user.full_name
    chat_id = update.effective_message.chat_id
    # В context обязательно нужно указывать id чата с пользователем
    # Более удобный способ отправки как по мне, особенно от лица модера
    context.bot.send_message(
        text='Добро пожаловать в бота',
        chat_id=chat_id
    )
    # Передаем данные в таблицу
    add_subscribers(
        tg_name=user,
        user_id=chat_id
    )


def main():
    # объек типа Bot нужен для работы с telegram API в более чистом виде, в сравнение с Update
    bot = Bot(token=TG_TOKEN)
    updater = Updater(bot=bot,
                     use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', do_start))
    # Создаем таблицу
    start_db()
    # Запуск скачиваний обновлений
    # idle() для того чтобы бот не завершился пока не обработает все данные
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
