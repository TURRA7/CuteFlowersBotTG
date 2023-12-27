
from dotenv import load_dotenv
from os import getenv
import asyncio
import sys

from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, select
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker
from sqlalchemy import BigInteger, URL, create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session, sessionmaker


# Загрузка параметров конфигурации из файла .env
load_dotenv()

engine = create_async_engine(getenv('SQLALCHEMY_URL'), echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = 'Products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    photo: Mapped[str] = mapped_column()


class Tools:
    @staticmethod
    async def add_item(name, description, price, photo):
        async with async_session() as conn:
            try:
                new_item = Product(name=name, \
                    description=description, price=price, photo=photo)
                conn.add(new_item)
                await conn.commit()
            except Exception as ex:
                print(ex)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
