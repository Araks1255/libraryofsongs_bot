from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Найти песню")],
    [KeyboardButton(text="Получить песни из альбома"), KeyboardButton(text="Получить группы жанра")],
    [KeyboardButton(text="Создать песню")],
    [KeyboardButton(text="Получить жанры"), KeyboardButton(text="Получить альбомы исполнителя")],
    [KeyboardButton(text="Найти альбом"), KeyboardButton(text="Найти исполнителя")]
],
                            resize_keyboard=True,
                            input_field_placeholder="Трунь")

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