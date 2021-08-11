
import requests
import telebot

from config import BOT_TOKEN, OPEN_WEATHER_TOKEN, URL_WEATHER, URL_GET_COORDS, URL_GET_CITY
from weather_bot_phrases import bot_phrases

bot = telebot.TeleBot(BOT_TOKEN)


def get_coords_from_text(message) -> dict:
    response = requests.get(
        URL_GET_COORDS.format(message.text, OPEN_WEATHER_TOKEN)
    )
    response_city_coord = response.json()
    coords = {
        'lat': response_city_coord[0]["lat"],
        'lon': response_city_coord[0]["lon"]
    }
    return coords


def get_weather_from_coords(coords: dict) -> dict:
    response = requests.get(
        URL_WEATHER.format(coords['lat'], coords['lon'], OPEN_WEATHER_TOKEN)
    )
    weather_data = response.json()
    return weather_data


def get_area_from_coords(coords: dict) -> str:
    response = requests.get(
        URL_GET_CITY.format(coords['lat'], coords['lon'], OPEN_WEATHER_TOKEN)
    )
    area_data = response.json()
    area = area_data[0]["name"]
    return area


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, bot_phrases["welcome_1"])


@bot.message_handler(commands=['help'])
def send_info(message):
    bot.send_message(message.chat.id, bot_phrases["help_1"])


@bot.message_handler(content_types=['text', 'location'])
def send_weather(message):
    try:
        if message.content_type == 'text':
            coords = get_coords_from_text(message)
            area = message.text
        else:
            coords = {
                'lat': message.location.latitude,
                'lon': message.location.longitude
            }
            area = get_area_from_coords(coords)
        weather_data = get_weather_from_coords(coords)

        weather_dict = {
            "weather": weather_data["daily"][0]["weather"][0]["main"],
            "temp_day": weather_data["daily"][0]["temp"]["day"],
            "temp_night": weather_data["daily"][0]["temp"]["night"],
            "feels_like_day": weather_data["daily"][0]["feels_like"]["day"],
            "feels_like_night": weather_data["daily"][0]["feels_like"]["night"],
            "humidity": weather_data["daily"][0]["humidity"],
            "wind_speed": weather_data["daily"][0]["wind_speed"]
        }
    except (IndexError, KeyError):
        bot.reply_to(message, bot_phrases["not_found_1"])
    else:
        bot.reply_to(message, bot_phrases["send_weather"].format(area, **weather_dict))


if __name__ == '__main__':
    bot.polling(none_stop=True)
