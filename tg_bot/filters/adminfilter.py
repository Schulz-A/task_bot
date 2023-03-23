from aiogram import types
from aiogram.filters import Filter

from tg_bot.config import Config


class AdminFilter(Filter):
    async def __call__(self, msg: types.Message, config: Config):
        return msg.from_user.id in config.tg_bot.admins
