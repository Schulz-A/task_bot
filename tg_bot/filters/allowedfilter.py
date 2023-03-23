from aiogram import types
from aiogram.filters import Filter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tg_bot.infrastructure.database.models.models import User


class AllowedFilter(Filter):
    async def __call__(self, message: types.Message, session: AsyncSession):

        user_id = int(message.from_user.id)
        stmt = select(User).where(User.id == user_id)
        user = await session.execute(stmt)
        result = user.scalars().first()
        if not result:
            return False

        return result.allow

