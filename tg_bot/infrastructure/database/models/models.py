from typing import Any

from sqlalchemy import Column, Integer, String, Boolean, Text, ARRAY, BigInteger, PickleType

from tg_bot.infrastructure.database.models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, unique=True)
    username = Column(String(255))
    full_name = Column(String(255), default=None)
    allow = Column(Boolean, default=False)
    referral_code = Column(String(255), default=None)
    bounty = Column(Integer, default=0)
    photo = Column(Boolean)


class Item(BaseModel):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(255))
    quantity = Column(Integer, default=0)
    descr = Column(Text())
    price = Column(Integer, default=0)
    photo_id = Column(String(255))

