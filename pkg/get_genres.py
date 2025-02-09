import requests
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from pkg.keyboards.keyboards import main

from envs.env import ROOT_URL

router = Router()

@router.message(StateFilter(None), F.text == "Получить жанры")
async def getting_genres(message: Message):
    try:
        response = requests.get(f"{ROOT_URL}/genres")
    except requests.exceptions.ConnectionError:
        await message.answer("Ошибка подключения к серверу", reply_markup=main)
        return
    
    genres = response.json()

    if len(genres) == 0:
        await message.answer("Ещё не создан ни один жанр, но вы можете это исправить :)", reply_markup=main)
        return

    i = 0
    while i < len(genres):
        await message.answer(genres[f"{i+1}"])
        i += 1

    await message.answer("Всё", reply_markup=main)