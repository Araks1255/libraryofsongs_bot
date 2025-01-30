import requests
import os
from requests_toolbelt import MultipartEncoder
from aiogram import F, Router, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from pkg.keyboards.keyboards import cancel_keyboard, yes_or_not, main

router = Router()
bot = Bot(token="7705741780:AAFqL0Bl-hlyTdXT-RWpssPU0RYmDlgFDvo")

class EmergingSong(StatesGroup):
    genre = State()
    band = State()
    album = State()
    song = State()
    song_file = State()
    verify = State()
    second_verify = State()

@router.message(StateFilter(None), F.text == "Создать песню")
async def start_creating_song(message: Message, state: FSMContext):
    await message.answer(
        text="Введите основной жанр, характерный для исполнителя",
        reply_markup=cancel_keyboard
    )
    await state.set_state(EmergingSong.genre)

@router.message(StateFilter(EmergingSong), F.text == "Отмена")
async def cancel(message:Message, state:FSMContext):
    await state.clear()
    await message.answer(
        "Ну нет так нет",
        reply_markup=main
    )

@router.message(EmergingSong.genre)
async def get_genre(message: Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await message.answer(
        text="Введите название группы или исполнителя"
    )
    await state.set_state(EmergingSong.band)

@router.message(EmergingSong.band)
async def get_band(message: Message, state: FSMContext):
    await state.update_data(band=message.text)
    await message.answer(
        text="Введите название альбома"
    )
    await state.set_state(EmergingSong.album)

@router.message(EmergingSong.album)
async def get_album(message: Message, state: FSMContext):
    await state.update_data(album=message.text)
    await message.answer(
        "Введите название песни"
    )
    await state.set_state(EmergingSong.song)

@router.message(EmergingSong.song)
async def get_song(message: Message, state: FSMContext):
    await state.update_data(song=message.text)
    global song_data
    song_data = await state.get_data()
    await message.answer(
        text=f"Жанр - {song_data["genre"]}\n"
            f"Исполнитель - {song_data["band"]}\n"
            f"Альбом - {song_data["album"]}\n"
            f"Песня - {song_data["song"]}\n\n"
            "Всё верно?",
            reply_markup=yes_or_not
    )
    await state.set_state(EmergingSong.verify)

@router.message(EmergingSong.verify, F.text == "Да")
async def song_is_correct(message: Message, state: FSMContext):
    await message.answer(
        "Отправьте файл с песней",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(EmergingSong.song_file)

@router.message(EmergingSong.song_file)
async def get_song_file(message: Message, state: FSMContext):
    try:
        file_id = message.audio.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
    except:
        await message.answer("Пожалуйста, отправьте файл с песней")

    global path_to_file_in_buffer
    path_to_file_in_buffer = f"H:/Мой диск/Проект пиотоновый/libraryofsongs_bot/buffer/creating/{song_data["song"]}.mp3"

    await bot.download_file(file_path, path_to_file_in_buffer)

    await message.answer(
        "Создать песню?",
        reply_markup=yes_or_not
    )

    await state.set_state(EmergingSong.second_verify)

@router.message(EmergingSong.verify, F.text == "Нет")
async def song_is_uncorrect(message: Message, state: FSMContext):
    await message.answer(
        "Ну ладно",
        reply_markup=main
    )
    await state.clear()
    return

@router.message(EmergingSong.second_verify, F.text == "Да")
async def all_song_is_correct(message: Message, state: FSMContext):
    file = open(path_to_file_in_buffer, "rb")
    form = MultipartEncoder(
        fields={
            "genre": song_data["genre"],
            "band": song_data["band"],
            "album": song_data["album"],
            "song": song_data["song"],
            "file": ("file", file, 'text/plain')
        }
    )

    try:
        request = requests.post("http://localhost:8080/songs/", data=form, headers={"Content-Type": form.content_type})
    except requests.exceptions.ConnectionError:
        await message.answer("Ошибка подключения к серверу", reply_markup=main)

    if request.status_code == 201:
        await message.answer("Песня успешно создана!", reply_markup= main)
    elif request.status_code == 422:
        await message.answer("Ошибка данных. Скорее всего, песня уже существует", reply_markup=main)
    else:
        await message.answer("Неизвестная ошибка", reply_markup=main)
    

    file.close()
    os.remove(path_to_file_in_buffer)

    await state.clear()

@router.message(EmergingSong.second_verify, F.text == "Нет")
async def all_song_is_correct(message: Message, state: FSMContext):
    await message.answer(
        "Ну ладно",
        reply_markup=main
    )
    await state.clear()
    return
