from core.settings import settings

import asyncio
import sys

from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, select
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker
from sqlalchemy import BigInteger, URL, create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import delete, func


engine = create_async_engine(settings.bots.sqlalchemy_url, echo=True)

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
            new_item = Product(name=name, \
                description=description, price=price, photo=photo)
            conn.add(new_item)
            await conn.commit()
     

    @staticmethod
    async def select_item():
        async with async_session() as conn:
            prod: dict = await conn.scalars(select(Product))
            return prod.all()

    @staticmethod
    async def del_item(itemID):
        async with async_session() as conn:
            await conn.execute(Product.__table__.delete().where(Product.id == itemID))
            await conn.commit()
         
      
            
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)