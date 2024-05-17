# Телеграм бот-витрина - CuteFlowers

Это приложение, представляет собой бот-витрину на тематику бисерых украшений. Приложение построено на языке **PYTHON** с использованием фреймворка **Aiogram3**.

## Структура проекта

```
.
└── CuteFlowers
    ├── core
    |   ├── __init__.py
    |   ├── content
    |   |       ├── __init__.py
    |   |       └── contents.py
    |   ├── database
    |   |       ├── __init__.py
    |   |       └── ADataBase.py
    |   ├── forms_state
    |   |       ├── __init__.py
    |   |       └── form_bot.py
    |   ├── handlers
    |   |       ├── __init__.py
    |   |       └── basic.py
    |   ├── keyboards
    |   |       ├── __init__.py
    |   |       └── reply_inline.py
    |   ├── utils
    |   |       ├── __init__.py
    |   |       └── commands.py
    |   ├── __init__.py
    |   ├── log_mod.py
    |   └── setup.cfg
    ├── app.py
    ├── docker-compose.yaml
    ├── Dockerfile
    ├── input
    ├── README.md
    ├── requirements.txt
    └── settings.py
```

___

### Краткое описание структуры

* **core**: Содержит пакеты для работы с ботом.
* **app.py**: Исполнительный файл проекта.
* **docker-compose.yaml**: Конфигурация docker-compose(запуск нескольких приложений в разных контейнерах вместе).
* **Dockerfile**: Конфигурация докера(инструкция для запуска контейнера с основным приложением).
* **input**: Файл с данными для подключения сторонних сервисов и токена бота.
* **README.md**: Файл описание проекта.
* **requirements.txt**:  Файл с описанием зависимостей.
* **settings.py**: Файл с классами для работы с конфигурационными данными.

___

### Инструменты использованные в проекте

![Static Badge](https://img.shields.io/badge/build-3.3.0-brightgreen?style=flat-square&logo=3.3.0&label=aiogram&labelColor=blue&color=gray)
![Static Badge](https://img.shields.io/badge/build-10.3.0-brightgreen?style=flat-square&logo=environs&label=environs&labelColor=%23BBC6C8&color=%23DDBEAA)
![Static Badge](https://img.shields.io/badge/build-2.9.9-brightgreen?style=flat-square&logo=psycopg2-binary&label=psycopg2-binary&labelColor=yellow&color=black)
![Static Badge](https://img.shields.io/badge/build-0.29.0-brightgreen?style=flat-square&logo=asyncpg&label=asyncpg&labelColor=%23469597&color=%23E5E3E4)
![Static Badge](https://img.shields.io/badge/build-2024.1-brightgreen?style=flat-square&logo=pytz&label=pytz&labelColor=%237b994f&color=%23f0dff2)


![Static Badge](https://img.shields.io/badge/python-7.0.0-badgeContent?style=flat&logo=Flake8&logoColor=%2381BECE&label=Flake8&labelColor=black&color=white)
![Static Badge](https://img.shields.io/badge/python-0.0.8-badgeContent?style=flat&logo=Flake8-annotations-complexity&logoColor=%2381BECE&label=Flake8-annotations-complexity&labelColor=%23A59CD3&color=%234B2D9F)
![Static Badge](https://img.shields.io/badge/python-24.2.6-badgeContent?style=flat&logo=Flake8_bugbear&logoColor=%2381BECE&label=Flake8_bugbear&labelColor=%23677C77&color=%23E0EFEA)
![Static Badge](https://img.shields.io/badge/python-2.3.0-badgeContent?style=flat&logo=Flake8_builtins&logoColor=%2381BECE&label=Flake8_builtins&labelColor=%23EFB9AD&color=%23BC0000)
![Static Badge](https://img.shields.io/badge/python-3.14.0-badgeContent?style=flat&logo=Flake8_comprehensions&logoColor=%2381BECE&label=Flake8_comprehensions&labelColor=%23ffef03&color=%23ca540c)
![Static Badge](https://img.shields.io/badge/python-2.1.0-badgeContent?style=flat&logo=Flake8_commas&logoColor=%2381BECE&label=Flake8_commas&labelColor=%23C9D46C&color=%23338309)
![Static Badge](https://img.shields.io/badge/python-1.7.0-badgeContent?style=flat&logo=Flake8_docstrings&logoColor=%2381BECE&label=Flake8_docstrings&labelColor=%23015366&color=%23A7D1D2)
![Static Badge](https://img.shields.io/badge/python-1.5.0-badgeContent?style=flat&logo=Flake8_eradicate&logoColor=%2381BECE&label=Flake8_eradicate&labelColor=%23CEAD6D&color=%23E1DCE0)
![Static Badge](https://img.shields.io/badge/python-0.18.2-badgeContent?style=flat&logo=Flake8_import_order&logoColor=%2381BECE&label=Flake8_import_order&labelColor=%23806491&color=%23B9848C)
![Static Badge](https://img.shields.io/badge/python-2.1.0-badgeContent?style=flat&logo=Flake8_pep3101&logoColor=%2381BECE&label=Flake8_pep3101&labelColor=%23BC2041&color=%239E8279)
![Static Badge](https://img.shields.io/badge/python-5.0.0-badgeContent?style=flat&logo=Flake8_print&logoColor=%2381BECE&label=Flake8_print&labelColor=%23F38307&color=%23D5F2ED)
![Static Badge](https://img.shields.io/badge/python-0.3.0-badgeContent?style=flat&logo=Flake8_rst_docstrings&logoColor=%2381BECE&label=Flake8_rst_docstrings&labelColor=%23DE60CA&color=%23882380)
![Static Badge](https://img.shields.io/badge/python-0.3.0-badgeContent?style=flat&logo=Flake8_string_format&logoColor=%2381BECE&label=Flake8_string_format&labelColor=%236B99C3&color=%23022E66)
![Static Badge](https://img.shields.io/badge/python-0.3.0-badgeContent?style=flat&logo=Flake8_string_format&logoColor=%2381BECE&label=Flake8_string_format&labelColor=%23dde4ea&color=%236e7478)
![Static Badge](https://img.shields.io/badge/python-0.0.6-badgeContent?style=flat&logo=Flake8_variables_names&logoColor=%2381BECE&label=Flake8_variables_names&labelColor=%23adbf8f&color=%23788e3c)
___

> ВАЖНО!: для назначения администратора, узнайте ваш id: https://t.me/getmyid_bot, далее вставьте полученый id в поле **ADMIN_ID** файла **input**.

___

## Инструкция по установке

1. После скачивания репозитория, распакуйте его в удобное место и откройте через ваш IDE.
2. Установка виртуальной среды и зависимостей:
    * Если ваш IDE - **VS CODE** или **PyCharm**, создайте виртуальную среду и установите зависимости с помощью файла requirements.txt
    * Если же вы пользуетесь другими IDE, откройте в корневом каталоге проекта 
    **PowerShell**, через shift+ПКМ(и выберите PowerShell).
        * Введите команду: ```python -m venv venv```
        * После установки среды, выполните её активацию: ```venv\Scripts\activate```
        * Далее установите зависимости: ```pip install -r requirements.txt```
3. В файле input добавьте необходимые конфигурационные данные (ВАЖНО: в параметре файла 'input', оставить значение 'postgres' - это название докер контейнера с PostgreSQL).
4. TOKEN бота вы можете найти в телеграм боте https://t.me/BotFather, выбрав в меню /newbot и пройдя процедуру его регистрации.
5. Далее для деплоя бота разместите папку с поректом на сервере, в файле docker-compose.yaml в параметре environment введите соответствующие данные, перейдите в рабочую директорию через терминал и выполните следующие команды:
    * Команда для сборки docker контейнера: ```docker-compose build``` # Дождитесь установки...
    * Команда для активации docker контейнера: ```docker-compose up``` # Проект запущен!

___

## Контакты

Моя почта: **turra777@mail.ru**

Мой телеграм: **https://t.me/chicano_712**
