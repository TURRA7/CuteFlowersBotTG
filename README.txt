RU:
Это простейшей телеграмм бот витрина.
Он позволяет админу добавлять и удалять товары,
а пользователю просматривать их и связываться с продавцом.

Библиотеки используемые в проекте:
1. Aiogram v.3
2. SQLAlchemy v.2
3. Asyncio
4. logging
5. sys
6. environs
7. dataclasses

Для работы бота, следует добавить в файл "input" соответствующие данные:
1. TOKEN - токен для бота, полученный у бота телеграмм: @BotFather
2. ADMIN_ID - Это "id" пользователя, который будет иметь доступ к
функциям администрирования бота. Получить "id" можно у бота: @getmyid_bot
3. SQLALCHEMY_URL - Здесь указывается ваше подключение к базе данных.
Оно может отличиться в зависимости от выбранной БД, доп. драйвера или
типа подключения...

Так же следует изменить данные в файле "contents" в словаре "message_dict",
в паре 18 и 19 для отображения ваших актуальных данных для пользователей
вашего бота.

ДОКУМЕНТАЦИЯ:

/////////////////////////////////////////////////////////////////////////////

Хэндлеры:

1. "get_start" - Обработчик команды start:
Выводит Смайлик, приветственное сообщение с указанием никнейма пользователя,
а так же клавиатуру, если пользователь является администратором, в клавиатуре
есть кнопка, которая открывает "админ-меню".

2. "start_bot" - Обработчик запуска бота:
Бот, присылает администратору оповещение о своём запуске.

3. "stop_bot" - Обработчик остановки бота:
Бот, присылает администратору оповещение о своём отключении.

4. "contacts_saler" - Обработчик кнопки "КОНТАКТЫ":
Показывает пользователю актуальные контакты продавца.

5. "admin_saler" - Обработчик меню для админа:
Открывает клавиатуру админ-меню.

6. "main_menu" - Обработчик кнопки "МЕНЮ":
При нажатии на кнопку, пользователю открывается стартовое меню.

7. "add_item" - Обработчик кнопки "ДОБАВИТЬ ТОВАР"(FSM):
Запускает машину состояний, выводит сообщение с просьбой ввести название
товара.

8. "add_item_name" - Обработчик(FSM) добавление названия:
Сохраняет название товара введенное пользователем в FSM, выводит
сообщение с просьбой добавить описание, переходит к следующему состоянию.

9. "add_item_description" - Обработчик(FSM) добавление описания:
Сохраняет описание товара введенное пользователем в FSM, выводит
сообщение с просьбой добавить цену, переходит к следующему состоянию.

10. "add_item_price" - Обработчик(FSM) добавление цены:
Сохраняет цену товара введенное пользователем в FSM, выводит
сообщение с просьбой добавить фото, переходит к следующему состоянию.

11. "add_item_photo" - Обработчик(FSM) добавление фото, сохранение в БД:
Сохраняет фото товара добавленное пользователем в FSM, сохраняет
полученный комплекс данных в базу данных, через объект класса "Tools".
Далее выводит сообщение об успешном добавлении товара. Завершает
машину состояний.

12. "item_catalog" - Обработчик кнопки "КАТАЛОГ":
Выводит каталог товаров, пользователю в формате:
1. Фото
2. Название
3. Описание
4. Цена
Если пользователь является администратором, то под каждым товаром, у него
есть кнопка "УДАЛИТЬ".

13. "delete_item" - Обработчик кнопки "УДАЛИТЬ":
Обработчик получает "id" товара, далее применяя метод "del_item",
класса "Tools", удаляет товар из бд и выводит пользователю оповещение
об успешном удалении.
/////////////////////////////////////////////////////////////////////////////

КЛАССЫ:

1. Form - Класс "машины состояний" имеющий переменные с состояниями.

2. Base - Базовый(родительский) класс, для построения таблицы в ООП.

3. Bots - Класс данных, имеющий 3 переменных:
1.bot_token - токен бота
2.admin_id - id администратора
3.sqlalchemy_url - ссылка на подключение базы данных

4. Tools - Класс для работы с базой данных:
Содержит 3 метода, для работы с базой данных через ООП:
1."add_item" - принимает 4 параметра:
1.name(str) - название товара
2.description(str) - описание товара
3.price(int) - цену товара
4.photo(str) - id фотографии
2."select_item" - берет из БД данные и возвращает
их в виде словаря.
3."del_item" - принимает 1 параметр(int) это id товара
и по этому параметру, удаляет товар из базы данных.

5. Product - Представление таблицы с товарами в виде ООП класса

6. Settings - Класс имеющий в себе экземпляр бота.

7. ReplyKeyBoards - Класс для работы с "Reply-клавиатурами":
Имеет 1 метод "create_keyboard_reply" - принимает список значений(str),
создаёт кнопки.

8. InlineKeyBoards - Класс для работы с "Inline-клавиатурами":
Имеет 1 метод "create_keyboard_inline" - принимает 2 параметра:
1.text(str) - текст внутри кнопки(название кнопки).
2.callbacks(str) - callback данные.
Создаёт кнопки.
/////////////////////////////////////////////////////////////////////////////

ФУНКЦИИ:

1. start - Функция содержит в себе комплекс мер, по работе бота:
1. Подключение логирования.
2. Создание экземпляра бота.
3. Создание экземпляра диспетчера.
4. Регистрация хэндлеров.
5. Вызов функции создания базы данных
6. Старт/остановка бота.

2. async_main - Создаёт базу данных, если её нет в системе.

3. set_commands - Функция содержит экземпляр бота в параметрах. Внутри функции
список команд, которые пользователь будет видеть нажав на кнопку "menu" в
своём интерфейсе телеграмма(пользуясь ботом).

4. get_settings - В функцию передаётся адрес файла "input", из которого
полученные параметры возвращаются через класс Settings.

/////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////

EN:
This is the simplest telegram bot storefront.
It allows admin to add and delete items,
and the user to view them and contact the seller.

Libraries used in the project:
1. Aiogram v.3
2. SQLAlchemy v.2
3. Asyncio
4. logging
5. sys
6. environs
7. dataclasses

For the bot to work, you should add the appropriate data to the "input" file:
1. TOKEN - the token for the bot, obtained from the telegram bot: @BotFather
2. ADMIN_ID - This is the "id" of the user who will have access to the
administration functions of the bot. The "id" can be obtained from the bot: @getmyid_bot
3. SQLALCHEMY_URL - This specifies your connection to the database.
It may differ depending on the selected database, additional driver or connection type....
connection type...

You should also change the data in the "contents" file in the "message_dict" dictionary,
in pairs 18 and 19 to display your actual data to the users
of your bot.

DOCUMENTATION:

/////////////////////////////////////////////////////////////////////////////

HANDLERS:

1. "get_start" - Handler for the start command:
Outputs a Smiley face, a welcome message with the user's nickname,
as well as the keyboard, if the user is an administrator, in the keyboard
there is a button that opens the "admin menu".

2. "start_bot" - Bot start handler:
The bot, sends the admin a notification of its launch.

3. "stop_bot" - Bot stop handler:
Bot, sends an alert to the administrator about its shutdown.

4. "contacts_saler" - "CONTACTS" button handler:
Shows the user the actual contacts of the seller.

5. "admin_saler" - Admin Menu Handler:
Opens the admin menu keyboard.

6. "main_menu" - MENU button handler:
When the button is clicked, the start menu is opened to the user.

7. "add_item" - Handler for the "add item"(FSM) button:
Starts the state machine, displays a message asking the user to enter the name of the
item.

8. "add_item_name" - Handler(FSM) add name:
Saves the item name entered by the user in the FSM, displays a
a message asking to add a description, proceeds to the next state.

9. "add_item_description" - Handler(FSM) add description:
Saves the item description entered by the user in the FSM, displays a
a message asking to add a price, moves to the next state.

10. "add_item_price" - Handler(FSM) add price:
Saves the price of the item entered by the user in the FSM, displays a
a message asking to add a photo, moves to the next state.

11. "add_item_photo" - Handler(FSM) add photo, save to database:
Saves the item photo added by the user to the FSM, saves the
the received data set into the database, through the object of class "Tools".
Then displays a message about successful addition of the product. Completes
state machine.

12. "item_catalog" - Handler of the button "CATALOG":
Outputs the item catalog, to the user in the format:
1. Photo
2. Title
3. Description
4. Price
If the user is an administrator, then under each product, he has
has a "DELETE" button under each item.

13. "delete_item" - Handler of the "DELETE" button:
The handler gets the "id" of the item, then applying the "del_item" method,
method of the "Tools" class, deletes the item from the database and displays a notification to the user
about successful deletion.
/////////////////////////////////////////////////////////////////////////////

CLASSES:

1. Form - Class of "state machine" having variables with states.

2. Base - Base (parent) class for building a table in OOP.

3. Bots - Data class with 3 variables:
1.bot_token - bot token
2.admin_id - admin id
3.sqlalchemy_url - link to database connection

4. Tools - Class for working with the database:
Contains 3 methods, for working with the database via OOP:
1. "add_item" - takes 4 parameters:
1.name(str) - item name
2.description(str) - product description
3.price(int) - price of the item
4.photo(str) - photo id
2. "select_item" - takes data from the database and returns it as a dictionary.
them in the form of a dictionary.
3. "del_item" - takes 1 parameter(int) is the id of the product.
and by this parameter, removes the item from the database.

5. Product - Representation of the table with goods in the form of OOP class

6. Settings - A class that has an instance of the bot.

7. ReplyKeyBoards - Class for working with "Reply-keyboards":
Has 1 method "create_keyboard_reply" - takes a list of values(str),
creates keys.

8. InlineKeyBoards - Class for working with "Inline-keyboards":
Has 1 method "create_keyboard_inline" - takes 2 parameters:
1.text(str) - text inside the key(name of the key).
2.callbacks(str) - callback data.
Creates buttons.
/////////////////////////////////////////////////////////////////////////////

FUNCTIONS:

1. start - The function contains a set of measures for the bot's operation:
1. Connection of logging.
2. Creating an instance of the bot.
3. Creating a dispatcher instance.
4. Registering the handlers.
5. Calling the database creation function
6. Start/stop the bot.

2. async_main - Creates a database if it does not exist in the system.

3. set_commands - The function contains the bot instance in parameters. Inside the function
a list of commands that the user will see by clicking on the "menu" button in the
in his Telegram interface (using the bot).

4. get_settings - The address of the "input" file is passed to the function, from which the received parameters are returned through the Settings class.
parameters are returned through the Settings class.

/////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////