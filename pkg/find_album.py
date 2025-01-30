import requests
import os
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.context import FSMContext

from pkg.keyboards.keyboards import cancel_keyboard

router = Router()

class FindingAlbum(StatesGroup):
    album = State()

@router.message(StateFilter(None), F.text == "Найти альбом")
async def finding_album(message: Message, state: FSMContext):
    await message.answer(
        text="Введите название альбома",
        reply_markup=cancel_keyboard
    )
    await state.set_state(FindingAlbum.album)

@router.message(StateFilter(FindingAlbum), F.text == "Отмена")
async def cancel(message:Message, state:FSMContext):
    await message.answer(
        "Ну нет так нет",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
    return

@router.message(FindingAlbum.album)
async def get_album(message: Message, state: FSMContext):
    desired_album = message.text

    url = f"http://localhost:8080/songs/album/{desired_album}"

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        await message.answer("Ошибка подключения к серверу",reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    
    album = response.json()
    if len(album) == 0:
        await message.answer(
            "Альбом не найден. Возможно, вы совершили опечатку, или его ещё не существует в нашей базе данных",
            reply_markup=ReplyKeyboardRemove()
            )
        await state.clear()
        return


    await message.answer(
        text="Альбом найден\n\n"
        f"Жанр - {album["genre"]}\n"
        f"Исполнитель - {album["band"]}\n"
        f"Название - {album["album"]}\n",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
