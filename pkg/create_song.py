import requests
from requests_toolbelt import MultipartEncoder
from aiogram import F, Router, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

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

@router.message(StateFilter(None), F.text == "Создать Песню")
async def order(message: Message, state: FSMContext):
    await message.answer(
        text="Введите основной жанр, характерный для исполнителя"
    )
    await state.set_state(EmergingSong.genre)

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
    global song_check
    song_check = await state.get_data()
    print(song_check)
    await message.answer(
        text=f"Жанр - {song_check["genre"]}\n"
            f"Исполнитель - {song_check["band"]}\n"
            f"Альбом - {song_check["album"]}\n"
            f"Песня - {song_check["song"]}\n\n"
            "Всё верно?"
    )
    await state.set_state(EmergingSong.verify)

@router.message(EmergingSong.verify, F.text == "Да")
async def song_is_correct(message: Message, state: FSMContext):
    await message.answer(
        "Отправьте файл с песней"
    )
    await state.set_state(EmergingSong.song_file)

@router.message(EmergingSong.song_file)
async def get_song_file(message: Message, state: FSMContext):
    file_id = message.audio.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    global path_to_file_in_buffer
    path_to_file_in_buffer = "H:/Мой диск/Проект пиотоновый/libraryofsongs_bot/buffer/" + song_check["song"] + ".mp3"
    await bot.download_file(file_path, path_to_file_in_buffer)
    await message.answer(
        "Создать песню?"
    )
    await state.set_state(EmergingSong.second_verify)

@router.message(EmergingSong.second_verify, F.text == "Да")
async def all_song_is_correct(message: Message, state: FSMContext):
    form = MultipartEncoder(
        fields={
            "genre": song_check["genre"],
            "band": song_check["band"],
            "album": song_check["album"],
            "song": song_check["song"],
            "file": ("file", open(path_to_file_in_buffer, "rb"), 'text/plain')
        }
    )
    request = requests.post("http://localhost:8080/songs/", data=form, headers={"Content-Type": form.content_type})