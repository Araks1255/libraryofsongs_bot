import requests
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from pkg.keyboards.keyboards import cancel_keyboard

router = Router()

class GettingSongsFromAlbum(StatesGroup):
    album = State()

@router.message(StateFilter(None), F.text == "Получить все песни из альбома")
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
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
    return

@router.message(GettingSongsFromAlbum.album)
async def get_songs(message: Message, state: FSMContext):
    desired_album = message.text

    try:
        response = requests.get(f"http://localhost:8080/songs/{desired_album}")
    except requests.exceptions.ConnectionError:
        await message.answer(
            "Ошибка подключения к серверу",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
        return
    
    bands = response.json()
    if len(bands) == 0:
        await message.answer("Альбом не найден. Возможно, вы совершили опечатку, или его ещё нет в нашей базе данных")
        await state.clear()
        return

    i = 0
    while i < len(bands):
        await message.answer(bands[f"{i+1}"])
        i += 1

    await message.answer("Это все существующие в нашей базе данных песни из этого альбома")
    await state.clear()