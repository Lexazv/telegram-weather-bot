from telebot import types


def get_additional_forecast_keyboard():
    """ 
    Generates inline keyboard.

    Returns:
        types.InlineKeyboardMarkup: additional forcast keyboard.
    """
    additional_forecast_keyboard = types.InlineKeyboardMarkup(row_width=1)
    three_days_btn = types.InlineKeyboardButton(
        "Get 3 days forecast", callback_data=3
    )
    five_days_btn = types.InlineKeyboardButton(
        "Get 5 days forecast", callback_data=5
    )
    additional_forecast_keyboard.add(three_days_btn, five_days_btn)
    return additional_forecast_keyboard


def get_forecast_keyboard():
    """ 
    Generates keyboard to get forecast by GPS.

    Returns:
        types.ReplyKeyboardMarkup: get forecast keyboard.
    """
    forecast_keyboard = types.ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True
    )
    get_forecast_btn = types.KeyboardButton(
        '\U0001F305 Get forecast', request_location=True
    )
    forecast_keyboard.add(get_forecast_btn)
    return forecast_keyboard
