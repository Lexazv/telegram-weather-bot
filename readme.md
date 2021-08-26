# Telegram Weather Bot description

[Weather Bot for Telegram. This Bot receives information from user and replies with weather forecast. </br>](https://t.me/oz_weather_bot)

Receives weather information from [OpenWeather](https://openweathermap.org/).

### Built with

- [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)

## Getting started
### Tokens
The first step to creating a Telegram Bot is getting a personal token **BOT_TOKEN**. 
It can be generated in Telegram by [BotFather](https://telegram.me/BotFather).

To make API calls, it`s necessary to have personal **OPEN_WEATHER_TOKEN**. 
It can be generated on [OpenWeather](https://openweathermap.org/) after creating an account.</br>

### Libraries and frameworks

Second step is installing PyTelegramBotAPI library. It`s needed to implement desirable Bot stucture and logic.</br>

- PyTelegramBotAPI installation:
```
pip install pyTelegramBotAPI
```
Next step is installing Flask to create Webhhoks.

- Flask installation:
```
pip install flask
```

Final step is installing Heroku to manage the deployment process.

- Heroku installation:
```
pip install heroku
```

### Config vars

Constants, used in this project, like tokens or URLs are not listed in any project file. 
They were added to [Heroku Dashboard](https://id.heroku.com/login). </br>
To access them from code, following constructions were used:
```
BOT_TOKEN = os.environ['BOT_TOKEN']
APP_URL = os.environ['APP_URL']
```
[More about creating and managing configuration vars](https://devcenter.heroku.com/articles/config-vars).

## Usage

### How to send information

There are three ways for user to send information:</br>

1. Send a city name (can be sent in any language, not only English).</br>
2. Send country code according to ISO 3166. [More about ISO 3166](https://www.iso.org/iso-3166-country-codes.html). </br>
3. Send GPS location.</br>

### Received information

Bot replies to user message by sending a daily weather forecast in **metric units** with information, listed below.</br>

- Location name
- General weather description
- Daily temperature 
    - How daily temperature feels like
- Night temperature
    - How night temperature feels like
- Humidity
- Wind speed

### Additional weather forecast

After receiving a daily weather forecast, it`s possible to choose an option on inline keyboard 
and get 3 or 5 days forecast for this location.

## Contact

Oleksii Zvedeniuk - zvedalex@gmail.com</br>

- Telegram: https://t.me/lexazv
- Linkedin: https://www.linkedin.com/in/oleksii-zvedeniuk-1b8a40215/


- Project GitHub link: https://github.com/Lexazv/Telegram_Weather_Bot
- Project Telegram link: https://t.me/oz_weather_bot