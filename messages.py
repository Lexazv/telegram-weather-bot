# Contains bot phrases.
messages = {
    "welcome_1": "Hi! I can help you to get a perfect weather forecast!\n"
                 "You can click on button to get forecast send me a city name.\n"
                 "Use /help if you need more information!",

    "help_1": "This Bot can send you a weather forecast for one day. There are three ways to get it.\n"
              "1. Send a city name.\nYou can do it not only in English, use any language you want.\n"
              "2. Send a country code according to ISO 3166.\n"
              "3. Send your GPS location. In that case, Bot will send you a forecast for your current location.\n"
              "Bot takes weather information from https://openweathermap.org/",

    "not_found_1": "Sorry! I have no information about this city. Try again or send me your GPS location.",

    "connection error": "Sorry! An unexpected error occured.\nPlease, try again later!",

    "send_weather": "{0}\n\nWeather forecast for {date}.\n\n{weather}.\n\n"
                    "Daily temperature around {temp_day}C°.\nFeels like {feels_like_day}C°.\n"
                    "Night temperature near {temp_night}C°. \nFeels like {feels_like_night}C°.\n\n"
                    "Humidity is {humidity}%.\nWind speed - {wind_speed} m\s."
}
