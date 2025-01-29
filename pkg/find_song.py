import requests
import os
from requests_toolbelt import MultipartEncoder
from aiogram import F, Router, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.context import FSMContext

from pkg.keyboards.keyboards import cancel_keyboard
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
    await state.clear()
    await message.answer(
        "Ну нет так нет",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(FindingSong.song)
async def get_song(message: Message, state: FSMContext):
    desired_song = message.text

    url = f"http://localhost:8080/songs/song/{desired_song}"
    response = requests.get(url)
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
        f"Название - {song_name}"
    )

    path_to_file = f"H:/Мой диск/Проект пиотоновый/libraryofsongs_bot/buffer/{song_name}.mp3"

    url = f"http://localhost:8080/songs/file/{genre}/{band}/{album}/{song_name}"
    response = requests.get(url)

    with open(path_to_file, "wb") as file:
        file.write(response.content)

    song_file = FSInputFile(path_to_file)
    await message.answer_audio(song_file)

    

