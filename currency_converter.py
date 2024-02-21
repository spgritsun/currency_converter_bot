import random
import telebot
from telebot import types
from extensions import CurrencyConverter, APIException, manual
from config import API_TOKEN

amount = 0
values = None

bot = telebot.TeleBot(API_TOKEN)
my_currency_converter = CurrencyConverter()


@bot.message_handler(commands=['start', 'hello'])
def start(message):
    first_name = message.from_user.first_name if message.from_user.first_name else ''
    last_name = message.from_user.last_name if message.from_user.last_name else ', друг мой'
    bot.send_message(message.chat.id, f'Привет, {first_name} {last_name}! 😄\nЯ бот, который умеет пересчитывать '
                                      f'курсы валют.🤑 \nСо списком команд можно ознакомиться здесь: /menu')
    bot.send_message(message.chat.id, 'Выберите пару валют для конвертации 😉', draw_buttons(message))


@bot.message_handler(commands=['values'])
def values(message):
    bot.send_message(message.chat.id, '<b>Список валют, доступных для конвертации в любом сочетании:</b>\n- <i>доллар '
                                      'США</i> (USD);\n- <i>евро</i> (EUR);\n- <i>российский рубль</i> (RUB).',
                     parse_mode='html')


@bot.message_handler(commands=['help'])
def values(message):
    bot.send_message(message.chat.id, manual, parse_mode='html')


@bot.message_handler(commands=['menu'])
def values(message):
    bot.send_message(message.chat.id,
                     'Список команд бота:\n/start и /hello - начало работы или перезапуск бота;\n/values - '
                     'список доступных валют;\n/help - инструкция по применению бота.')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global values
    values = call.data.split('/')
    bot.send_message(call.message.chat.id, 'Введите сумму, которую хотите пересчитать')
    bot.register_next_step_handler(call.message, amount_of_money)


def amount_of_money(message):
    global amount
    try:
        amount = float(message.text.strip().replace(',', '.'))
    except APIException('Неверный ввод суммы пользователем'):
        bot.send_message(message.chat.id, '🙅‍♂ ‍Неверный ввод суммы! Введите правильную сумму, пожалуйста.')
        bot.register_next_step_handler(message, amount_of_money)
        return
    if amount > 0:
        result = my_currency_converter.get_price(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'✅  {result} \n\t Хотите продолжить?')
        bot.send_message(message.chat.id, 'Выберите, пожалуйста, пару валют 😄', draw_buttons(message))

    else:
        try:
            if amount == 0:
                raise APIException('Введена нулевая сумма конвертации')
            elif amount < 0:
                raise APIException('Введена отрицательная сумма конвертации')
        except APIException:
            bot.send_message(message.chat.id,
                             f'{message.from_user.first_name}... 😜 Пошутили и хватит! Введите, пожалуйста, число, '
                             f'которое больше ноля.')
            bot.register_next_step_handler(message, amount_of_money)


def draw_buttons(message):
    phrases = ['Что и во что будем конвертировать? 😊', 'Что и во что будем пересчитывать? 😄',
               'Что и во что переводим? 😉']
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('RUB -> USD', callback_data='RUB/USD')
    button2 = types.InlineKeyboardButton('RUB -> EUR', callback_data='RUB/EUR')
    button3 = types.InlineKeyboardButton('USD -> RUB', callback_data='USD/RUB')
    button4 = types.InlineKeyboardButton('EUR -> RUB', callback_data='EUR/RUB')
    button5 = types.InlineKeyboardButton('USD -> EUR', callback_data='USD/EUR')
    button6 = types.InlineKeyboardButton('EUR -> USD', callback_data='EUR/USD')
    markup.add(button1, button2, button3, button4, button5, button6)
    bot.send_message(message.chat.id, f'{random.choice(phrases)}', reply_markup=markup)


bot.polling(none_stop=True)
