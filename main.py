import traceback  # импорт модуля для извлечения, форматирования и вывода на печать трассировок стека
import telebot  # импорт модуля для работы Telegramm-бота
from extensions import MoneyConverter, APIException  # импорт классов из файла extensions.py
from config import TOKEN, exchanges  # импорт токена и списка валют из файла config.py


bot = telebot.TeleBot(TOKEN)  # инициализация бота


@bot.message_handler(commands=['start'])  # обработчик сообщений начала работы бота
def start(message: telebot.types.Message):
    text = 'Бот приветствует тебя!\n' \
           'Я умею конвертировать валюты!\n' \
           'Хочешь ознакомиться с правилами? Жми: /help\n' \
           'Хочешь увидеть список доступных валют? Жми: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])  # обработчик сообщений инструкций по правилам пользования
def help(message: telebot.types.Message):
    text = 'Для конвертации валют введи:\n' \
           'валюту, цену которой хочешь узнать\n' \
           'валюту, в которой надо узнать цену первой валюты\n' \
           'количество первой валюты\n' \
           'Например: доллар рубль 100\n' \
           'Чтобы увидеть список доступных валют нажми: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])  # обработчик сообщений доступных валют
def values(message: telebot.types.Message):
    text = 'Можно сконвертировать:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)
    help_ = 'Всё ещё нужна помощь? Жми: /help'
    bot.send_message(message.chat.id, help_)


@bot.message_handler(content_types=['text'])  # обработчик сообщений для конвертации валют и отлавливания ошибок
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Введите 3 параметра!')
        answer = MoneyConverter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f'\n{e}')

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Ошибка обработки \n{e}')
    else:
        bot.reply_to(message, answer)


bot.polling()  # метод для постоянной работы бота
