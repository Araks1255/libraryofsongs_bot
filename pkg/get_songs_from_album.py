import requests
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from pkg.keyboards.keyboards import cancel_keyboard, main

from envs.env import ROOT_URL

router = Router()

class GettingSongsFromAlbum(StatesGroup):
    album = State()

@router.message(StateFilter(None), F.text == "Получить песни из альбома")
async def getting_songs_from_album(message: Message, state: FSMContext):
    await message.answer(
        "Введите альбом, песни из которого желаете получить",
        reply_markup=cancel_keyboard
    )
    await state.set_state(GettingSongsFromAlbum.album)

@router.message(StateFilter(GettingSongsFromAlbum), F.text == "Отмена")
async def cancel(message:Message, state:FSMContext):
    await message.answer(
        "Ну нет так нет",
        reply_markup=main
    )
    await state.clear()
    return

@router.message(GettingSongsFromAlbum.album)
async def get_songs(message: Message, state: FSMContext):
    desired_album = message.text

    try:
        response = requests.get(f"{ROOT_URL}/{desired_album}")
    except requests.exceptions.ConnectionError:
        await message.answer(
            "Ошибка подключения к серверу",
            reply_markup=main
        )
        await state.clear()
        return
    
    bands = response.json()
    if len(bands) == 0:
        await message.answer("Альбом не найден. Возможно, вы совершили опечатку, или его ещё нет в нашей базе данных", reply_markup=main)
        await state.clear()
        return

    i = 0
    while i < len(bands):
        await message.answer(bands[f"{i+1}"])
        i += 1

    await message.answer("Всё", reply_markup=main)
    await state.clear()