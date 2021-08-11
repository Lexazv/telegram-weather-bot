#Telegram Weather Bot description

---
Test version of Telegram Weather Bot. This Bot receives information from user and replies with daily weather forecast.</br>

Currently in development, using [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI). </br>

This Bot receives weather information from [OpenWeather](https://openweathermap.org/).
##How to send information

---
There are three ways for user to send information:</br>

1. Send a city name (can be sent in any language, not only English).</br>
2. Send country code according to ISO 3166. [More about ISO 3166](https://www.iso.org/iso-3166-country-codes.html). </br>
3. Send GPS location.</br>
##Received information

---
Bot replies to user message by sending a daily weather forecast in **metric units** with information, listed below.</br>

- Location name
- General weather description
- Daily temperature 
    - How daily temperature feels like
- Night temperature
    - How night temperature feels like
- Humidity
- Wind speed
##Config file description

---
###Config file structure:

```
BOT_TOKEN = <...>
OPEN_WEATHER_TOKEN = <...>
URL_WEATHER = <...>
URL_GET_COORDS = <...>
URL_GET_CITY = <...>
```
Personal **BOT_TOKEN** was generated in Telegram app by [BotFather](https://telegram.me/BotFather). </br>

To make API calls, it`s necessary to have personal **OPEN_WEATHER_TOKEN**. 
It can be generated on [OpenWeather](https://openweathermap.org/) after creating an account.</br>

API call can be made by sending a request to specific URL. Each API has it`s own specific URL.</br>

**URL_WEATHER, URL_GET_COORDS**, **URL_GET_CITY** are examples of links for different APIcalls.</br>

After choosing an API, it`s possible to get URL template.</br>

[List of available APIs](https://openweathermap.org/api). </br>