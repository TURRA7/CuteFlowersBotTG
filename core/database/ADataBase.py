"""
Модуль с инструментами по работе с базой данных.

В данном модуле, используется диалект PostgreSQL.
Данный модуль, содержит логирование.

classes:
    AioDataBase: Родительский класс с инициализации параметров
    подключения и работы с базой данных: conn и cursor.
    DataBaseTools: Класс с инструментами по работе с БД.

methods:
    create_table: Создаёт заданные таблицы в базе данных(если их нет).
    delete_table: Удаляет таблицу по переданому названию.
    insert_item: Добавление данных в таблицу по названию таблицы
    и самим аргументам.
    fetch_all_items_cat: Получение данных из таблицы по
    переданому параметру категории
    fetch_all_items: Получение данных из конкретного столбца таблицы,
    по названию таблицы и названию столбца.
    delete_item: Удаление данных из таблицы по id.
    select_item_id: Получение данных из таблицы по id.
"""

import os
import psycopg2

from ..log_mod import Logger

# Создание логгера
db_logger = Logger("log_db.log")
logger = db_logger.get_logger()


class AioDataBase:
    """Базовый класс для работы с базой данных."""

    def __init__(self):
        """Метод инициализации переменных."""
        self.conn = psycopg2.connect(dbname=os.getenv('DB_NAME'),
                                     user=os.getenv('USER'),
                                     password=os.getenv('PASSWORD'),
                                     host=os.getenv('HOST'),
                                     port=5432,
                                     client_encoding="utf8")
        self.cursor = self.conn.cursor()


class DataBaseTools(AioDataBase):
    """Класс содержит инструменты для работы с базой данных."""

    def __init__(self):
        """Метод инициализации переменных."""
        super().__init__()

    def create_table(self):
        """Метод создания таблиц(если таковые отсутствуют)."""
        create_table_command = """
        CREATE TABLE IF NOT EXISTS goods (
            id SERIAL PRIMARY KEY,
            title VARCHAR(35) NOT NULL,
            description VARCHAR(100) NOT NULL,
            price INTEGER CHECK (price >= 0),
            category INTEGER CHECK (category BETWEEN 1 AND 4),
            photo VARCHAR(255) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            id_user VARCHAR(100) NOT NULL
        );
        """
        try:
            self.cursor.execute(create_table_command)
            self.conn.commit()
            logger.info("Таблицы users и goods - созданы!")
        except Exception as ex:
            logger.info("Ошибка создания таблиц: %s", ex)

    def delete_table(self, table_name: str):
        """
        Метод удаления таблицы.

        params:
            table_name: название таблицы в виде строки.
        """
        delete_table_command = f"""DROP TABLE IF EXISTS {table_name}"""
        try:
            self.cursor.execute(delete_table_command)
            self.conn.commit()
            logger.info("Таблица %s - удалена!", table_name)
        except Exception as ex:
            logger.info("Ошибка удаления таблицы: %s", ex)

    def insert_item(self, table_name: str, **kwargs):
        """
        Метод добавления данных в таблицу.

        params:
            table_name: название таблицы в виде строки.
            kwargs: столбец таблицы=значение.
        """
        keys = ', '.join(kwargs.keys())
        values = ', '.join('%s' for _ in kwargs)
        insert_item_command = f"""
        INSERT INTO {table_name} ({keys})
        VALUES ({values})
        """
        try:
            self.cursor.execute(insert_item_command, list(kwargs.values()))
            self.conn.commit()
            logger.info("Данные добавлены в таблицу %s", table_name)
        except Exception as ex:
            logger.info("Ошибка добавления данных! %s", ex)

    def fetch_all_items_cat(self, table_name: str, cat_item: int):
        """
        Метод получения элементов из таблицы по категории.

        params:
            table_name: Название таблицы.
            cat_item: Категория товаров.
        """
        fetch_all_command = f"""
        SELECT * FROM {table_name} WHERE category = %s
        """
        try:
            self.cursor.execute(fetch_all_command, (cat_item,))
            rows = self.cursor.fetchall()
            logger.info("Данные получены!")
            return rows
        except Exception as ex:
            logger.info("Ошибка получения данных из таблицы: %s", ex)
            return []

    def fetch_all_items(self, table_name: str, column: str):
        """
        Метод для получения всех элементов столбца из таблицы.

        params:
            table_name: Название таблицы.
            column: Столбец данные из которого необходимо получить.
        """
        fetch_all_command = f""" SELECT {column} FROM {table_name} """
        try:
            self.cursor.execute(fetch_all_command)
            rows = self.cursor.fetchall()
            logger.info("Данные получены!")
            result = [int(row[0]) for row in rows]
            return result
        except Exception as ex:
            logger.info("Ошибка получения данных из таблицы: %s", ex)
            return []

    def delete_item(self, id_item: int):
        """
        Метод для удаления товара из базы данных по id.

        params:
            id_item: id товара.
        """
        delete_item_command = """
        DELETE FROM goods WHERE id = %s
        """
        try:
            self.cursor.execute(delete_item_command, (id_item,))
            self.conn.commit()
            logger.info("Товар с id: %s удалён!", id_item)
        except Exception as ex:
            logger.info("Ошибка удаления данных из таблицы: %s", ex)
            return []

    async def select_item_id(self, id_item: int):
        """
        Метод получения товара из базы данных по id.

        params:
            id_item: id товара.
        """
        select_item_command = """
        SELECT * FROM goods WHERE id = %s
        """
        try:
            self.cursor.execute(select_item_command, (id_item,))
            rows = self.cursor.fetchone()
            return rows
        except Exception as ex:
            logger.info("Ошибка получения данных из таблицы: %s", ex)
            return []
