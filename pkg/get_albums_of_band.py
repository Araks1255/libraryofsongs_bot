import requests
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from pkg.keyboards.keyboards import cancel_keyboard, main

router = Router()

class GettingAlbumsOfBand(StatesGroup):
    band = State()

@router.message(StateFilter(None), F.text == "Получить альбомы исполнителя")
async def getting_albums_of_band(message: Message, state: FSMContext):
    await message.answer(
        "Введите исполнителя, альбомы которого хотите найти",
        reply_markup=cancel_keyboard
    )
    await state.set_state(GettingAlbumsOfBand.band)

@router.message(StateFilter(GettingAlbumsOfBand), F.text == "Отмена")
async def cancel(message:Message, state:FSMContext):
    await message.answer(
        "Ну нет так нет",
        reply_markup=main
    )
    await state.clear()
    return

@router.message(GettingAlbumsOfBand.band)
async def get_albums(message: Message, state: FSMContext):
    desired_band = message.text

    try:
        response = requests.get(f"http://localhost:8080/songs/albums/{desired_band}")
    except requests.exceptions.ConnectionError:
        await message.answer(
            "Ошибка подключения к серверу",
            reply_markup=main
        )
        await state.clear()
        return
    
    albums = response.json()
    if len(albums) == 0:
        await message.answer("Исполнитель не найден, возможно, вы опечатались, или его ещё нет в базе данных", reply_markup=main)
        await state.clear()
        return

    i = 0
    while i < len(albums):
        await message.answer(albums[f"{i+1}"])
        i += 1

    await message.answer("Это все альбомы данной группы, существующие в нашей базе данных", reply_markup=main)
    await state.clear()