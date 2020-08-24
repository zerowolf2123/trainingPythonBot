from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TG_TOKEN = '13477144:Axu7x9Atuk_FQe0XMDa9lzVTw2PY'
# Наши клавиши
BUTTON_HELPS = 'Помощь'

# Клавиши работают как и обычные сообщения, при нажатии на них в чат будет отправлено сообщение с текстом с клавиши

def option_buttons():
    # Клавиши мы объявляем как и Inline кнопки, только без колбэков и ссылок
    keyboard = [
        [
            KeyboardButton(BUTTON_HELPS)
        ]
    ]
    # Возвращаем клавиатуру
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        # Динамически подгоняет размеры клавиатуры
        resize_keyboard=True
    )


def start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(text='''Добро пожаловать в чат.
Воспользуйтесь командой /help чтобы узнать больше''',
                                        # Вызываем нашу сетку
                                        reply_markup=option_buttons())


def do_help(update: Update, context: CallbackContext):
    update.effective_message.reply_text(text='''Напишите что угодно чтобы спрятать клавиатуру''')


def do_echo(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    context.bot.send_message(
        chat_id=chat_id,
        text="Спрятали клавиатуру\n\nНажмите /start чтобы вернуть её обратно",
        reply_markup=ReplyKeyboardRemove(),
    )


def main():
    bot = Bot(token=TG_TOKEN)
    updater = Updater(bot=bot,
                      use_context=True,)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', do_help))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, do_echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
