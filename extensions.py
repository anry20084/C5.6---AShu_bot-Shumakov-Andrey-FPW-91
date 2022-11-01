import requests  # импорт модуля для отправки всех видов HTTP-запросов
import json  # импорт модуля для парсинга полученных ответов
from config import exchanges, header  # импорт списка валют из файла config.py


class APIException(Exception):  # класс исключений
    pass


class MoneyConverter(Exception):                    # класс отправки запросов к API со статическим методом get_price(),
    @staticmethod                                   # который отлавливает ошибки, а также принимает три аргумента
    def get_price(base, quote, amount):             # и возвращает сообщение со стоимостью конвертации
        try:
            base_ticker = exchanges[base]
        except KeyError:
            raise APIException(f'Ошибка обработки валюты - {base}')

        try:
            quote_ticker = exchanges[quote]
        except KeyError:
            raise APIException(f'Ошибка обработки валюты - {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Ошибка обработки количества - {amount}')

        if base_ticker == quote_ticker:
            raise APIException('Нет смысла в этом действии!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}',
                         header)

        price = round(json.loads(r.content)[quote_ticker] * amount, 2)
        message = f'Цена {amount} {exchanges[base]} в {exchanges[quote]} составила {price} {exchanges[quote]}'
        return message
