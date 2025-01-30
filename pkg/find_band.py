import requests
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from pkg.keyboards.keyboards import cancel_keyboard, main

router = Router()

class FindingBand(StatesGroup):
    band = State()

@router.message(StateFilter(None), F.text == "Найти исполнителя")
async def finding_album(message: Message, state: FSMContext):
    await message.answer(
        text="Введите название группы или имя исполнителя",
        reply_markup=cancel_keyboard
    )
    await state.set_state(FindingBand.band)

@router.message(StateFilter(FindingBand), F.text == "Отмена")
async def cancel(message:Message, state:FSMContext):
    await message.answer(
        "Ну нет так нет",
        reply_markup=main
    )
    await state.clear()
    return

@router.message(FindingBand.band)
async def get_band(message: Message, state: FSMContext):
    desired_band = message.text

    url = f"http://localhost:8080/songs/band/{desired_band}"

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        await message.answer("Ошибка подключения к серверу",reply_markup=main)
        await state.clear()
        return
    
    band = response.json()
    if len(band) == 0:
        await message.answer(
            "Группа не найдена. Возможно, вы совершили опечатку, или её ещё не существует в нашей базе данных",
            reply_markup=main
            )
        await state.clear()
        return


    await message.answer(
        text="Исполнитель найден\n\n"
        f"Жанр - {band["genre"]}\n"
        f"Имя исполнителя/название группы - {band["band"]}",
        reply_markup=main
    )
    await state.clear()