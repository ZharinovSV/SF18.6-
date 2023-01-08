import requests
import json
from config import *


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: int):
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        if amount <= 0:
            raise APIException('Введите количество больше 0')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}&apikey={APIKEY}")
        d = json.loads(r.content)
        total_base = round(float(d[quote_ticker]) * amount, 5)

        return total_base