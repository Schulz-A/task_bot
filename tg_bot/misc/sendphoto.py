from aiogram import Bot
from aiogram.types import InputFile, BufferedInputFile


async def send_local_photo(bot: Bot, file_path: str, chat_id: int, caption: str = None):
    with open(file_path, "rb") as photo:
        photo = BufferedInputFile(photo, filename="wssw")
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)