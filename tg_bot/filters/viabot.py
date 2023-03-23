from aiogram import types
from aiogram.filters import Filter

from tg_bot.config import Config


class ViaBotFilter(Filter):
    async def __call__(self, msg: types.Message, config: Config):
        return msg.via_bot
