import telebot
import requests

botTimeWeb = telebot.TeleBot('7923775487:AAFq_Qyh5WzRWnus8iR3dCh4LxmPuRR7da4')

from telebot import types


@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"<b>{message.from_user.first_name}</b>, привет!\nЗа какой период ты хочешь получить статистику сайта?"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_today = types.KeyboardButton(text='За сегодня')
    button_yes = types.KeyboardButton(text='За определённое время')
    markup.add(button_today, button_yes)
    botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)


@botTimeWeb.message_handler(func=lambda message: True)
def handle_message(message):
    visits = 0
    views = 0
    if message.text == "За определённое время":
        botTimeWeb.send_message(message.chat.id,
                                "Введите две даты в формате (гггг-мм-дд), разделенные запятой (например: 2025-02-01,2025-03-01):")
        botTimeWeb.register_next_step_handler(message, get_dates)

    elif message.text == "За сегодня":
        # Запрос статистики за сегодня
        OAUTH_TOKEN = 'y0__xDh3sSaAhj80zUg1diVtRIzlCiJwXpDSdjc3xB4FPlq75vD_w'
        COUNTER_ID = '99820869'
        date_today = '2025-03-01'  # Замените на текущую дату

        # URL для запроса к API Яндекс.Метрики
        API_URL = f'https://api-metrika.yandex.net/stat/v1/data'

        # Параметры запроса
        params = {
            'ids': COUNTER_ID,
            'metrics': 'ym:s:visits,ym:s:pageviews',
            'dimensions': 'ym:s:date',
            'date1': date_today,  # Начальная дата
            'date2': date_today,  # Конечная дата
            'accuracy': 'full'
        }

        # Заголовки запроса
        headers = {
            'Authorization': f'OAuth {OAUTH_TOKEN}'
        }

        # Отправка запроса
        response = requests.get(API_URL, headers=headers, params=params)

        # Обработка ответа
        if response.status_code == 200:
            data = response.json()
            stats_message = "Статистика за сегодня:\n"
            for item in data['data']:
                stats_message += (f"Дата: {item['dimensions'][0]['name']}, "
                                  f"Посещения: {item['metrics'][0]}, "
                                  f"Просмотры страниц: {item['metrics'][1]}\n")
                visits += int(item['metrics'][0])
                views += int(item['metrics'][1])
            botTimeWeb.send_message(message.chat.id, stats_message)
        else:
            botTimeWeb.send_message(message.chat.id, f"Ошибка {response.status_code}: {response.text}")

        second_mess = f"Всего посещений: {int(visits)}\n" \
                      f"Всего просмотров страниц: {int(views)}"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Назад"))  # Кнопка "Назад"
        markup.add(types.InlineKeyboardButton("Перейти на сайт", url="https://chemistrypro.onrender.com/"))
        botTimeWeb.send_message(message.chat.id, second_mess, reply_markup=markup)

    elif message.text == "Назад":
        startBot(message)


def get_dates(message):
    try:
        visits = 0
        views = 0
        date1, date2 = map(str.strip, message.text.split(','))

        OAUTH_TOKEN = 'y0__xDh3sSaAhj80zUg1diVtRIzlCiJwXpDSdjc3xB4FPlq75vD_w'
        COUNTER_ID = '99820869'

        # URL для запроса к API Яндекс.Метрики
        API_URL = f'https://api-metrika.yandex.net/stat/v1/data'

        # Параметры запроса
        params = {
            'ids': COUNTER_ID,
            'metrics': 'ym:s:visits,ym:s:pageviews',
            'dimensions': 'ym:s:date',
            'date1': date1,  # Начальная дата
            'date2': date2,  # Конечная дата
            'accuracy': 'full'
        }

        # Заголовки запроса
        headers = {
            'Authorization': f'OAuth {OAUTH_TOKEN}'
        }

        # Отправка запроса
        response = requests.get(API_URL, headers=headers, params=params)

        # Обработка ответа
        if response.status_code == 200:
            data = response.json()
            stats_message = "Статистика:\n"
            for item in data['data']:
                stats_message += (f"Дата: {item['dimensions'][0]['name']}, "
                                  f"Посещения: {item['metrics'][0]}, "
                                  f"Просмотры страниц: {item['metrics'][1]}\n")
                visits += int(item['metrics'][0])
                views += int(item['metrics'][1])
            botTimeWeb.send_message(message.chat.id, stats_message)
        else:
            botTimeWeb.send_message(message.chat.id, f"Ошибка {response.status_code}: {response.text}")

        second_mess = f"Всего посещений: {int(visits)}\n" \
                      f"Всего просмотров страниц: {int(views)}"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Назад"))  # Кнопка "Назад"
        markup.add(types.InlineKeyboardButton("Перейти на сайт", url="https://chemistrypro.onrender.com/"))
        botTimeWeb.send_message(message.chat.id, second_mess, reply_markup=markup)

    except Exception as e:
        botTimeWeb.send_message(message.chat.id,
                                "Ошибка при вводе дат. Пожалуйста, попробуйте еще раз в формате (гггг-мм-дд, гггг-мм-дд).")


botTimeWeb.infinity_polling()