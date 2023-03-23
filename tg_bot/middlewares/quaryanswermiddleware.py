from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery


class CBQAnswerMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
                       event: CallbackQuery,
                       data: Dict[str, Any]
                       ) -> Any:
        result = await handler(event, data)
        await event.answer()
        return result
