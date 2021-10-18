from datetime import date

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