import os

from telebot import types, TeleBot
from flask import Flask, request
from requests.exceptions import HTTPError

from url_functions import get_weather_from_coords, get_area_from_coords, \
    get_coords_from_text
from messages import messages
from bot_methods import parse_weather
from keyboards import get_additional_forecast_keyboard, \
    get_forecast_keyboard


BOT_TOKEN = os.environ['BOT_TOKEN']
APP_URL = os.environ['APP_URL']


bot = TeleBot(BOT_TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Sends answer to "/start" command.

    :param message: "/start" command, sent by user

    :return: None
    """
    bot.send_message(
        message.chat.id, messages["welcome_1"], 
        reply_markup=get_forecast_keyboard()
    )


@bot.message_handler(commands=['help'])
def send_info(message):
    """
    Sends answer to "/help" command.

    :param message: "/help" command, sent by user

    :return: None
    """
    bot.send_message(message.chat.id, messages["help_1"])


@bot.message_handler(content_types=['text', 'location'])
def send_weather(message):
    """
    Sends weather forecast.

    :param message: city name, code or location, sent by user

    :raises: exceptions, listed in url_functions.py

    :return: None
    """
    try:
        if message.content_type == 'text':
            area = message.text
            coords = get_coords_from_text(area)

        else:
            coords = {
                'lat': message.location.latitude,
                'lon': message.location.longitude
            }
            area = get_area_from_coords(coords)

        weather_json_response = get_weather_from_coords(coords)
        weather_info = parse_weather(weather_json_response)

    except (KeyError, HTTPError):
        bot.send_message(message.chat.id, messages["not_found_1"])

    except ConnectionError:
        bot.send_message(message.chat.id, messages["connection error"])

    else:
        bot.send_message(
            message.chat.id, messages["send_weather"].format(area, **weather_info), 
            reply_markup=get_additional_forecast_keyboard()
        )


@bot.callback_query_handler(func=lambda call: True)
def send_additional_forecast(call):
    """
    Sends forecast if user used inline keyboard.

    :param call: user`s choice on inline keyboard

    :raises exceptions, listed in url_functions.py

    :return: None
    """
    try:
        area = call.message.text.split("\n")[0]
        coords = get_coords_from_text(area)

        weather_json_response = get_weather_from_coords(coords)

        days = 1
        while days <= int(call.data):
            weather_info = parse_weather(weather_json_response, days)
            bot.send_message(
                call.message.chat.id, 
                messages["send_weather"].format(area, **weather_info)
            )
            days += 1

    except (KeyError, HTTPError):
        bot.send_message(call.message.chat.id, messages["not_found_1"])
        
    except ConnectionError:
        bot.send_message(call.message.chat.id, messages["connection error"])


@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL + BOT_TOKEN)
    return "!", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
