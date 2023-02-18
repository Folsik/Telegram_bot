###  Description

This is bot for barbershop.
This bot shows service  barbershops, administers group of telegrams and, 
in the administrator model, has the ability to add and remove services.

### Dependencies
This bot written on language Python 3, using the library "aiogram" and base of data "sqlite"

### Manual for starting
You need to find in the telegram "BotFather" write him the command "/start" 
then "/new bot". Next, you need to come up with a name and a username, 
that should contain bot. At the end you will be given the "HTTP API" 
this key needs to be inserted in the "TOKEN" field.
This bot has possibility administration groups therefore for correct 
operation you need to create a group and give administrator rights this bot. 
To get started enter the command "/start"

### Manual for using
In user mode there are commands, linked to buttons.
"Time_work" - time work this barbershop
"Address" - exact location this barbershop
"Service" - all services this barbershop
In the mode administration there are two commands linked to buttons
"Download" - this commands adds new services by step starting from 
the picture ending with the price and skids it's in the database
"Delete" - completely removes the service
To enter the administrator mode, you need to enter the command in the 
group chat "/moderator" you will be automatically transferred to the bot setup.
Command "/moderator" it will work for everyone with "group administrator" access rights


### Описание
Это бот для barbershop.
Этот бот показывает услуги barbershop, управляет группой телеграмм канала и,
в режиме администратора, имеет возможность добавлять и удалять услуги.

### Зависимости
Этот бот написан на языке Python 3 с использованием библиотеки "aiogram" и базы данный "sqlite"


### Инструкции для запуска
Вам нужно найти в telegram "BotFather" написать ему команду "/start" 
затем "/newbot". Далее вам нужно придумать имя и имя пользователя, 
которое должно содержать bot. В конце вам дадут "HTTP API" этот ключ 
нужно вставить в поле "TOKEN".
Этот бот имеет возможность администрирования групп, поэтому для корректной
работы вам необходимо создать группу и предоставить права администратора этому боту.
Для начала работы введите команду "/start"

### Инструкция по использованию
В пользовательском режиме есть команды, которые привязаны к кнопкам.
"Time_work" - время работы barbershop
"Address" - точное местоположение barbershop
"Service" - все услуги barbershop
В режиме администрирования есть две команды, которые так же привязаны к кнопкам.
"Download" - эта команда пошагово добавляет новые услуги, начиная с
картинки и заканчивая ценой, и заносит ее в базу данных.
"Delete" - полностью удаляет услугу.
Чтобы перейти в режим администратора, вам необходимо ввести команду в
групповом чате "/moderator", вы будете автоматически переведены в настройки бота.
Команда "/moderator" будет работать для всех, у кого есть права доступа "администратор группы".