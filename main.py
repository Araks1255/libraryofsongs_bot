import asyncio
import logging

logging.basicConfig(level=logging.INFO)

from aiogram import Bot, Dispatcher

from pkg import create_song

async def main():
    bot = Bot(token="7705741780:AAFqL0Bl-hlyTdXT-RWpssPU0RYmDlgFDvo")
    dp = Dispatcher()
    dp.include_routers(
        create_song.router
        )
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())