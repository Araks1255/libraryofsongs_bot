import requests
import os
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from pkg.keyboards.keyboards import cancel_keyboard, main

from envs.env import PATH_TO_PROJECT, ROOT_URL

router = Router()

class FindingSong(StatesGroup):
    song = State()

@router.message(StateFilter(None), F.text == "Найти песню")
async def finding_song(message: Message, state: FSMContext):
    await message.answer(
        text="Введите название песни",
        reply_markup=cancel_keyboard
    )
    await state.set_state(FindingSong.song)

@router.message(StateFilter(FindingSong), F.text == "Отмена")
async def cancel(message:Message, state:FSMContext):
    await message.answer(
        "Ну нет так нет",
        reply_markup=main
    )
    await state.clear()
    return

@router.message(FindingSong.song)
async def get_song(message: Message, state: FSMContext):
    desired_song = message.text

    url = f"{ROOT_URL}/song/{desired_song}"

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        await message.answer("Ошибка подключения к серверу",reply_markup=main)
        await state.clear()
        return

    if response.status_code == 200:
        song = response.json()

        genre = song["genre"]
        band = song["band"]
        album = song["album"]
        song_name = song["song"]

        await message.answer(
            text="Песня найдена\n\n"
            f"Жанр - {genre}\n"
            f"Исполнитель - {band}\n"
            f"Альбом - {album}\n"
            f"Название - {song_name}",
            reply_markup=main
        )
    elif response.status_code == 404:
        await message.answer("Песня не найдена. Возможно вы опечатались, или её ещё не существует в базе данных.",reply_markup=main)
        await state.clear()
        return

    path_to_file = f"{PATH_TO_PROJECT}/buffer/getting/{song_name}.mp3"

    url = f"{ROOT_URL}/file/{genre}/{band}/{album}/{song_name}"

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        await message.answer("Ошибка подключения к серверу",reply_markup=main)
        await state.clear()
        return

    with open(path_to_file, "wb") as file:
        file.write(response.content)

    song_file = FSInputFile(path_to_file)
    await message.answer_audio(song_file)

    os.remove(path_to_file)
    await state.clear()