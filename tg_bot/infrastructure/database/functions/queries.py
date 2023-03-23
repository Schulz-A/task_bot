from sqlalchemy import select, update, or_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import contains

from tg_bot.infrastructure.database.models.models import User, Item


async def add_user(session: AsyncSession, ids, username, fullname, photo, allow=False):
    insert_stmt = insert(User).values(
        id=ids,
        username=username,
        full_name=fullname,
        allow=allow,
        photo=photo
    ).on_conflict_do_nothing().returning(User.id)
    result = await session.execute(insert_stmt)
    await session.commit()
    return result.scalars().first()


async def fetch_all_users(session: AsyncSession):
    n = select(User)
    result = await session.execute(n)
    await session.commit()
    return result.scalars().all()


async def fetch_user(session: AsyncSession, *clauses):
    stmt = select(User).where(*clauses)
    result = await session.execute(stmt)
    user = result.scalars().first()
    return user


async def update_user(session: AsyncSession, *clauses, **kwargs):
    stmt = update(User).where(*clauses).values(**kwargs)
    await session.execute(stmt)
    await session.commit()


async def add_items(session: AsyncSession, item_name: str, quantity: int, descr: str, price: int, photo_url: str):
    insert_stmt = insert(Item).values(
        name=item_name,
        quantity=quantity,
        descr=descr,
        price=price,
        photo_id=photo_url
    ).on_conflict_do_nothing().returning(Item.name)
    result = await session.execute(insert_stmt)
    await session.commit()
    return result.scalars().first()


async def get_item(session: AsyncSession, *clauses):
    n = select(Item).where(*clauses)
    result = await session.execute(n)
    await session.commit()
    return result.scalars().first()


async def get_items_by(session: AsyncSession, text):
    stmt = select(Item).filter(or_(Item.name.ilike(f"%{text}%"), Item.discr.ilike(f"%{text}%"))).order_by(Item.name)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_all_items(session: AsyncSession):
    stmt = select(Item).order_by(Item.name)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalars().all()


async def update_item(session: AsyncSession, *clauses, **params):
    stmt = update(Item).where(*clauses).values(params)
    result = await session.execute(stmt)
    await session.commit()


async def get_items(session: AsyncSession, *clauses):
    stmt = select(Item).where(*clauses)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_item_columns(session: AsyncSession, *columns):
    stmt = select(*columns).order_by(Item.name)
    result = await session.execute(stmt)
    await session.commit()
    return result.fetchall()


async def reset_quantity_column(session: AsyncSession):
    stmt = update(Item).values(quantity=0)
    await session.execute(stmt)
    await session.commit()
