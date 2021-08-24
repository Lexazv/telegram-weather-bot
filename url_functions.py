import os

import requests
from requests import exceptions
from boto.s3.connection import S3Connection

from config import OPEN_WEATHER_TOKEN, URL_GET_WEATHER, URL_GET_COORDS, URL_GET_AREA


OPEN_WEATHER_TOKEN = S3Connection(os.environ[OPEN_WEATHER_TOKEN])
URL_GET_WEATHER = S3Connection(os.environ[URL_GET_WEATHER])
URL_GET_COORDS = S3Connection(os.environ[URL_GET_COORDS])
URL_GET_AREA = S3Connection(os.environ[URL_GET_AREA])


def get_coords_from_text(message) -> dict:
    """
    Returns latitude and longitude of the city entered by the user.

    :param message: city name or ISO 3166 city code, sent by user.
    :type message: str

    :raises HTTPError: if user send non-existing city
    :raises ConnectionError: if wrong URL_GET_COORDS

    :rtype: dict
    :return: dict with city latitude and longitude
    """
    response = requests.get(
        URL_GET_COORDS.format(message, OPEN_WEATHER_TOKEN)
    )
    response_city_coord = response.json()

    if response_city_coord == [] or response.status_code == 404:
        raise exceptions.HTTPError

    coords = {
        'lat': response_city_coord[0]["lat"],
        'lon': response_city_coord[0]["lon"]
    }
    return coords


def get_weather_from_coords(coords: dict) -> dict:
    """
    Returns response with weather information from latitude and longitude.

    :param coords: city coordinates
    :type coords: dict

    :raises HTTPError: if coords are wrong
    :raises ConnectionError: if wrong URL_GET_WEATHER

    :rtype: dict
    :return: json-formatted response from URL_GET_WEATHER
    """
    response = requests.get(
        URL_GET_WEATHER.format(coords['lat'], coords['lon'], OPEN_WEATHER_TOKEN)
    )

    response.raise_for_status()

    weather_json_response = response.json()
    return weather_json_response


def get_area_from_coords(coords: dict) -> str:
    """
    Returns area name from latitude and longitude.

    :param coords: city coordinates
    :type coords: dict

    :raises ConnectionError: if wrong URL_GET_AREA
    :raises HTTPError: if area not found

    :rtype: str
    :return: area name
    """
    response = requests.get(
        URL_GET_AREA.format(coords['lat'], coords['lon'], OPEN_WEATHER_TOKEN)
    )

    response.raise_for_status()

    area_data = response.json()
    area = area_data[0]["name"]
    return area
