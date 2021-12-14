import os
from requests.exceptions import HTTPError

from telebot import types, TeleBot
from flask import Flask, request

import bot_methods
import url_functions
from messages import messages
from keyboards import get_add_keyboard, get_main_keyboard


BOT_TOKEN = os.environ.get('BOT_TOKEN')
APP_URL = os.environ.get('APP_URL')


bot = TeleBot(BOT_TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """ Send welcome message """
    bot.send_message(
        message.chat.id, messages["welcome"], reply_markup=get_main_keyboard()
    )


@bot.message_handler(commands=['help'])
def send_info(message):
    """ Send help message """
    bot.send_message(message.chat.id, messages["help"])


@bot.message_handler(content_types=['text', 'location'])
def send_forecast(message):
    """ Send weather forecast """
    try:
        if message.content_type == 'text':
            area = message.text
            coords = url_functions.get_coords_from_text(area)
        else:
            coords = {
                'lat': message.location.latitude, 
                'lon': message.location.longitude
            }
            area = url_functions.get_area_name_from_coords(coords)
        weather_data = url_functions.get_weather_data_from_coords(coords)
        forecast = bot_methods.parse_weather_data(weather_data)
    except (KeyError, HTTPError, ConnectionError):
        bot.send_message(message.chat.id, messages["not_found"])
    else:
        bot.send_message(
            message.chat.id, messages["send_weather"].format(area, **forecast), 
            reply_markup=get_add_keyboard()
        )


@bot.callback_query_handler(func=lambda call: True)
def send_additional_forecast(call):
    """ Send additional weather forecast """
    try:
        area = call.message.text.split("\n")[0]
        coords = url_functions.get_coords_from_text(area)
        weather_data = url_functions.get_weather_data_from_coords(coords)
        days = 1
        while days <= int(call.data):
            weather_info = bot_methods.parse_weather_data(weather_data, days)
            bot.send_message(
                call.message.chat.id, 
                messages["send_weather"].format(area, **weather_info)
            )
            days += 1
    except (KeyError, HTTPError, ConnectionError):
        bot.send_message(call.message.chat.id, messages["not_found"])   


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
