from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TG_TOKEN = '1347447144:AAExu7x9Atuk_FQe0IozXMDa9lzVT8kw2PY'


def do_func_text(update: Update, context: CallbackContext):
    update.effective_message.reply_text(text='''*MARKDOWN*
/bold1 -- жирный шрифт
/italic1 -- наклонный шрифт
/url1 -- ссылка в тексте без превью
/urlpr1 -- ссылка в тексте с превью
/code1 -- отображение кода в тексте
*HTML*
/bold2 -- жирный шрифт
/italic2 -- наклонный шрифт
/url2 -- ссылка в тексте без превью
/urlpr2 -- ссылка в тексте с превью
/code2 -- отображение кода в тексте
/photo -- сообщение с фото''',
                                        parse_mode=ParseMode.MARKDOWN)


def do_Markdown_bold1(update: Update, context: CallbackContext):
    # *...* - выделяет все жирным текстом
    update.effective_message.reply_text('В данном сообщение показаны *слова написанные жирным текстом*',
                                        # ParseMode - нужен для искажения текста
                                        parse_mode=ParseMode.MARKDOWN)


def do_italic1(update: Update, context: CallbackContext):
    # _ ... _  делает наклонный текст
    update.effective_message.reply_text('''В данном сообщение показаны _слова написанные под наклоном_
`Примечание:` нельзя писать _*жирным текстом*_ *_под наклоном_*''',
                                        parse_mode=ParseMode.MARKDOWN)


def do_Markdown_url1(update: Update, context: CallbackContext):
    # [...](ссылка) - заменяет ссылку на текст в []
    update.effective_message.reply_text('''Ссылка на мою страницу в вк: [мое вк](https://vk.com/juvotnoe)
Без превью''',
                                        parse_mode=ParseMode.MARKDOWN,
                                        # Убирает превью ссылки
                                        disable_web_page_preview=True)


def do_Markdown_url_pr1(update: Update, context: CallbackContext):
    update.effective_message.reply_text('''Ссылка тг канал с халявой: [халява](https://t.me/sharewoodbiz)
С превью''',
                                        parse_mode=ParseMode.MARKDOWN,
                                        disable_web_page_preview=False)


def do_Markdown_code1(update: Update, context: CallbackContext):
    # ` ... ` - выделяет однострочный текст особым цветом
    # ``` ... ``` - выделяет многострочный текст особым текстом
    update.effective_message.reply_text('''Главная строка этой функции:
`def do_Markdown_code1(update: Update, context: CallbackContext):`

Вся функция: 
```@debug_requests
def do_Markdown_code1(update: Update, context: CallbackContext):
    update.effective_message.reply_text(..., parse_mode=ParseMode.MARKDOWN)```''',
                                        parse_mode=ParseMode.MARKDOWN)


def do_HTML_bold2(update: Update, context: CallbackContext):
    # ParseMode.HTML - Использует элементы HTML
    update.effective_message.reply_text('''В данном сообщение показаны <b>слова написанные жирным текстом</b>
На HTML''',
                                        parse_mode=ParseMode.HTML)


def do_HTML_italic2(update: Update, context: CallbackContext):
    update.effective_message.reply_text('''В данном сообщение показаны <i>слова написанные под наклоном</i>
На HTML''',
                                        parse_mode=ParseMode.HTML)


def do_HTML_url2(update: Update, context: CallbackContext):
    update.effective_message.reply_text('''Ссылка на мою страницу в вк: <a href="https://vk.com/juvotnoe">Мое вк</a>
Без превью
На HTML''',
                                        parse_mode=ParseMode.HTML,
                                        disable_web_page_preview=True)


def do_HTML_url_pr2(update: Update, context: CallbackContext):
    update.effective_message.reply_text('''ССсылка тг канал с халявой: <a href="https://t.me/sharewoodbiz">халява</a>
С превью
На HTML''',
                                        parse_mode=ParseMode.HTML,
                                        disable_web_page_preview=False)


def do_HTML_code2(update: Update, context: CallbackContext):
    update.effective_message.reply_text('''Главная строка этой функции:
<code>def do_Markdown_code1(update: Update, context: CallbackContext):</code>

Вся функция: 
<pre>@debug_requests
def do_Markdown_code1(update: Update, context: CallbackContext):
    update.effective_message.reply_text(..., parse_mode=ParseMode.HTML)</pre>''',
                                        parse_mode=ParseMode.HTML)


def do_HTML_photo(update: Update, context: CallbackContext):
    # Так можно прикреплять фото к постам или сообщениям
    # &#8205; - это ''
    # Обязательно перед ссылкой на фото должен находится хоть какой нибудь текст
    update.effective_message.reply_text('''Здравствуйте <a href="https://izobrazhenie.net/uploads/photos/show/2461_713574610.jpg">&#8205;</a>
На данном фото расположен очень красивый мост, в насыщенных тонах''',
                                        parse_mode=ParseMode.HTML,
                                        disable_web_page_preview=False)


def main():
    bot = Bot(token=TG_TOKEN)
    updater = Updater(bot=bot,
                      use_context=True,)
    updater.dispatcher.add_handler(CommandHandler('start', do_func_text))
    updater.dispatcher.add_handler(CommandHandler('bold1', do_Markdown_bold1))
    updater.dispatcher.add_handler(CommandHandler('italic1', do_italic1))
    updater.dispatcher.add_handler(CommandHandler('url1', do_Markdown_url1))
    updater.dispatcher.add_handler(CommandHandler('urlpr1', do_Markdown_url_pr1))
    updater.dispatcher.add_handler(CommandHandler('code1', do_Markdown_code1))
    updater.dispatcher.add_handler(CommandHandler('bold2', do_HTML_bold2))
    updater.dispatcher.add_handler(CommandHandler('italic2', do_HTML_italic2))
    updater.dispatcher.add_handler(CommandHandler('url2', do_HTML_url2))
    updater.dispatcher.add_handler(CommandHandler('urlpr2', do_HTML_url_pr2))
    updater.dispatcher.add_handler(CommandHandler('code2', do_HTML_code2))
    updater.dispatcher.add_handler(CommandHandler('photo', do_HTML_photo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
