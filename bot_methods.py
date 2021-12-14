from datetime import date

def parse_weather_data(weather_json_response, days=0):
    """ Parse URL_GET_WEATHER response """
    forecast = {
        "date": date.fromtimestamp(weather_json_response["daily"][days]["dt"]),
        "weather": weather_json_response["daily"][days]["weather"][0]["main"],
        "temp_day": round(weather_json_response["daily"][days]["temp"]["day"], 1),
        "temp_night": round(weather_json_response["daily"][days]["temp"]["night"], 1),
        "feels_like_day": round(weather_json_response["daily"][days]["feels_like"]["day"], 1),
        "feels_like_night": round(weather_json_response["daily"][days]["feels_like"]["night"], 1),
        "humidity": weather_json_response["daily"][days]["humidity"],
        "wind_speed": weather_json_response["daily"][days]["wind_speed"]
    }
    return forecast
