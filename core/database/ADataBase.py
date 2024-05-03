import psycopg2
import logging
from logging.handlers import RotatingFileHandler

from settings import settings


# Создание логгера
logger = logging.getLogger('log_db.log')
logger.setLevel(logging.DEBUG)
# Создание обработчика консоли и установка уровеня отладки
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# Создание форматтера
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Добавить форматтер в ch
ch.setFormatter(formatter)
# Добавлении ротации логов
file_handler = RotatingFileHandler('log_db.log',
                                   maxBytes=1024 * 1024,
                                   backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
# Добавить ch в логгер, создание ротации
logger.addHandler(ch)
logger.addHandler(file_handler)


class AioDataBase:
    """Базовый класс для работы с базой данных."""
    def __init__(self):
        self.conn = psycopg2.connect(dbname=settings.bots.dbname,
                                     user=settings.bots.user,
                                     password=settings.bots.password,
                                     host=settings.bots.host,
                                     port=5432,
                                     client_encoding="utf8")
        self.cursor = self.conn.cursor()


class DataBaseTools(AioDataBase):
    """Класс содержит инструменты для работы с базой данных."""
    def __init__(self):
        """Метод инициализации переменных."""
        super().__init__()

    def create_table(self):
        """Метод создания таблиц."""
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
            name VARCHAR(100) NOT NULL
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
            logger.info(f"Таблица {table_name} - удалена!")
        except Exception as ex:
            logger.info("Ошибка удаления таблицы: %s", ex)

    def insert_item(self, table_name: str, **kwargs):
        """Метод добавления данных в таблицу."""
        keys = ', '.join(kwargs.keys())
        values = ', '.join('%s' for _ in kwargs)
        insert_item_command = f"""
        INSERT INTO {table_name} ({keys})
        VALUES ({values})
        """
        try:
            self.cursor.execute(insert_item_command, list(kwargs.values()))
            self.conn.commit()
            logger.info("Товар добавлен в таблицу", table_name)
        except Exception as ex:
            logger.info("Ошибка добавления товара! %s", ex)

    def update_item(self):
        """Метод изменения данных из таблицы."""
        pass

    def execute_item(self):
        """Метод выполнения запроса в БД."""
        pass
