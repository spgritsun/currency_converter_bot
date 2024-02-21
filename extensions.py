import requests
import json


class CurrencyConverter:
    @classmethod
    def get_price(cls, amount=1, base='EUR', quote='RUB'):
        r = requests.get(
            f'https://api.exchangeratesapi.io/v1/convert?access_key=01052f62fbe32a74cc2159647ef536d2&from={base}&to={quote}&amount={amount}')
        texts = json.loads(r.content)
        result = f'{amount} {base} - это {round(texts["result"], 2)} {quote}'
        return result


class APIException(Exception):
    pass


manual = '  <b>Инструкция по применению бота</b>\n1. <u>Список используемых команд:</u>\n- /start и /hello - начало работы и ' \
         'перезапуск бота;\n- /help - инструкция по применению бота;\n- /values - список доступных валют;\n- /menu - список ' \
         'используемых команд.\n2. <u>Порядок работы с ботом:</u>\n- нажатием кнопки с соответствующей надписью выбрать пару' \
         ' валют для конверации;\n- ввести сумму валюты, которую необходимо конвертировать;\n- получить результат.\n '
