import os

import requests
from requests import exceptions

OPEN_WEATHER_TOKEN = os.environ['OPEN_WEATHER_TOKEN']
URL_GET_WEATHER = os.environ['URL_GET_WEATHER']
URL_GET_COORDS = os.environ['URL_GET_COORDS']
URL_GET_AREA = os.environ['URL_GET_AREA']


def get_coords_from_text(message) -> dict:
    """ Get area coords """
    response = requests.get(URL_GET_COORDS.format(message, OPEN_WEATHER_TOKEN))
    response_json = response.json()
    if not response_json or response.status_code == 404:
        raise exceptions.HTTPError
    coords = {'lat': response_json[0]["lat"], 'lon': response_json[0]["lon"]}
    return coords


def get_weather_data_from_coords(coords: dict) -> dict:
    """ Get weather data from area chords """
    response = requests.get(
        URL_GET_WEATHER.format(coords['lat'], coords['lon'], OPEN_WEATHER_TOKEN)
    )
    response.raise_for_status()
    weather_data = response.json()
    return weather_data


def get_area_name_from_coords(coords: dict) -> str:
    """ Get area name from area coords """
    response = requests.get(
        URL_GET_AREA.format(coords['lat'], coords['lon'], OPEN_WEATHER_TOKEN)
    )
    response.raise_for_status()
    area_name = response.json()[0].get('name')
    return area_name
