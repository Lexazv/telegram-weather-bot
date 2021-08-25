import logging
from datetime import date

import telebot
from telebot import types
from flask import Flask, request

from url_functions import *
from weather_bot_phrases import bot_phrases

BOT_TOKEN = os.environ['BOT_TOKEN']
APP_URL = os.environ['APP_URL']


bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)


logging.basicConfig(
    level=logging.DEBUG,
    filename="weather_bot_logfile.log",
    filemode="a",
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def parse_weather(weather_json_response, days=0):
    """
    Parses URL_GET_WEATHER response.

    :param weather_json_response: json-formatted response from URL_GET_WEATHER
    :type weather_json_response: dict
    :param days: number of days, user wants to know about, days=0 means present day
    :type days: int

    :raises KeyError: if wrong weather_json_response

    :rtype: dict
    :return: weather information, which will be sent to user
    """
    weather_info = {
        "date": date.fromtimestamp(weather_json_response["daily"][days]["dt"]),
        "weather": weather_json_response["daily"][days]["weather"][0]["main"],
        "temp_day": round(weather_json_response["daily"][days]["temp"]["day"], 1),
        "temp_night": round(weather_json_response["daily"][days]["temp"]["night"], 1),
        "feels_like_day": round(weather_json_response["daily"][days]["feels_like"]["day"], 1),
        "feels_like_night": round(weather_json_response["daily"][days]["feels_like"]["night"], 1),
        "humidity": weather_json_response["daily"][days]["humidity"],
        "wind_speed": weather_json_response["daily"][days]["wind_speed"]
    }
    return weather_info


def generate_markup():
    """
    Generates inline keyboard.

    :return: markup
    """
    markup = types.InlineKeyboardMarkup(row_width=1)
    start_button = types.InlineKeyboardButton(
        "Get 3 days forecast", callback_data=3
    )
    help_button = types.InlineKeyboardButton(
        "Get 5 days forecast", callback_data=5
    )
    markup.add(start_button, help_button)
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Sends answer to "/start" command.

    :param message: "/start" command, sent by user

    :return: None
    """
    bot.send_message(message.chat.id, bot_phrases["welcome_1"])


@bot.message_handler(commands=['help'])
def send_info(message):
    """
    Sends answer to "/help" command.

    :param message: "/help" command, sent by user

    :return: None
    """
    bot.send_message(message.chat.id, bot_phrases["help_1"])


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

    except (KeyError, exceptions.HTTPError):
        bot.reply_to(message, bot_phrases["not_found_1"])
    except ConnectionError:
        logging.critical("Wrong URL request")
        bot.reply_to(message, bot_phrases["connection error"])
    else:
        logging.debug("User`s request")
        bot.reply_to(message, bot_phrases["send_weather"].format(area, **weather_info), reply_markup=generate_markup())


@bot.callback_query_handler(func=lambda call: True)
def send_additional_forecast(call):
    """
    Sends forecast if user used inline keyboard.

    :param call: user`s choice on inline keyboard

    :raises exceptions, listed in url_functions.py

    :return: None
    """
    try:
        logging.debug("User`s request")
        area = call.message.text.split("\n")[0]
        coords = get_coords_from_text(area)

        weather_json_response = get_weather_from_coords(coords)

        days = 1
        while days <= int(call.data):
            weather_info = parse_weather(weather_json_response, days)
            bot.send_message(call.message.chat.id, bot_phrases["send_weather"].format(area, **weather_info))
            days += 1

    except (KeyError, exceptions.HTTPError):
        bot.reply_to(call.message, bot_phrases["not_found_1"])
    except ConnectionError:
        logging.critical("Wrong URL request")
        bot.reply_to(call.message, bot_phrases["connection error"])


@app.route("/" + BOT_TOKEN, methods=["POST"])
def get_update():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL.format(BOT_TOKEN))
    return "!", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
