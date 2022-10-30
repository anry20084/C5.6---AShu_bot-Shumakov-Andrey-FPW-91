import requests  # импорт модуля для отправки всех видов HTTP-запросов
import json  # импорт модуля для парсинга полученных ответов
from config import exchanges  # импорт списка валют из файла config.py


class APIException(Exception):  # класс исключений
    pass


class MoneyConverter(Exception):                    # класс отправки запросов к API со статическим методом get_price(),
    @staticmethod                                   # который отлавливает ошибки, а также принимает три аргумента
    def get_price(base, quote, amount):             # и возвращает сообщение со стоимостью конвертации
        try:
            base_ticker = exchanges[base.lower()]
        except KeyError:
            raise APIException(f'Ошибка обработки валюты - {base}')

        try:
            quote_ticker = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f'Ошибка обработки валюты - {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Ошибка обработки количества - {amount}')

        if base_ticker == quote_ticker:
            raise APIException('Нет смысла в этом действии!')

        header = {'apikey': 'NZyY3M9ZJ6gEIdgN1yhbNnF0bPdOXq9n'}
        r = requests.get(f'https://api.apilayer.com/currency_data/live?base={base_ticker}&symbols={quote_ticker}',
                         header)

        price = json.loads(r.content)['quotes'][base_ticker + quote_ticker] * amount
        price = round(price, 2)
        message = f'Цена {amount} {exchanges[base]} в {exchanges[quote]} составила {price} {exchanges[quote]}'
        return message
