from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message

from pkg.keyboards.keyboards import main

router = Router()

@router.message(StateFilter(None), F.text == "/start")
async def salute(message: Message):
    await message.answer(
        text="Этот бот предоставляет доступ к моему пет-проекту - простенькому api для хранения музыки. Приятного пользования!",
        reply_markup=main
    )