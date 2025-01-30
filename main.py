import asyncio
import logging

logging.basicConfig(level=logging.INFO)

from aiogram import Bot, Dispatcher

from pkg import create_song, find_song, get_genres, get_bands_by_genre, get_albums_of_band, get_songs_from_album, find_album, find_band, saluting

from envs.env import TOKEN

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(
        create_song.router,
        find_song.router,
        get_genres.router,
        get_bands_by_genre.router,
        get_albums_of_band.router,
        get_songs_from_album.router,
        find_album.router,
        find_band.router,
        saluting.router
        )
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())