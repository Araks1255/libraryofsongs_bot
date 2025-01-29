from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

cancel_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отмена")]
],
                            resize_keyboard=True,
                            input_field_placeholder="Вводить тут")

yes_or_not = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Нет"), KeyboardButton(text="Да")]
],
                            one_time_keyboard=False,
                            resize_keyboard=True,
                            input_field_placeholder="Отвечай")