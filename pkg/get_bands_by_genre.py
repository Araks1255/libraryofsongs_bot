import requests
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from pkg.keyboards.keyboards import cancel_keyboard, main

from envs.env import ROOT_URL

router = Router()

class GettiingBandByGenre(StatesGroup):
    genre = State()

@router.message(StateFilter(None), F.text == "Получить группы жанра")
async def getting_bands_by_genre(message: Message, state: FSMContext):
    await message.answer(
        "Введите жанр, по которому хотите найти исполнителей",
        reply_markup=cancel_keyboard
    )
    await state.set_state(GettiingBandByGenre.genre)

@router.message(StateFilter(GettiingBandByGenre), F.text == "Отмена")
async def cancel(message:Message, state:FSMContext):
    await message.answer(
        "Ну нет так нет",
        reply_markup=main
    )
    await state.clear()
    return

@router.message(GettiingBandByGenre.genre)
async def get_bands(message: Message, state: FSMContext):
    desired_genre = message.text

    try:
        response = requests.get(f"{ROOT_URL}/bands/{desired_genre}")
    except requests.exceptions.ConnectionError:
        await message.answer(
            "Ошибка подключения к серверу",
            reply_markup=main
        )
        await state.clear()
        return
    
    bands = response.json()
    if len(bands) == 0:
        await message.answer("Группы, исполняющие в данном жанре не найдены. Возможно, вы совершили опечатку, или жанр ещё не добавлен", reply_markup=main)
        await state.clear()
        return

    i = 0
    while i < len(bands):
        await message.answer(bands[f"{i+1}"])
        i += 1

    await message.answer("Всё", reply_markup=main)
    await state.clear()
    