# Yatube
## Социальная сеть для публикации личных дневников
### Описание
API для социальной Yatube
### Технологии
Python 3.7
Django 2.2.16
### Запуск проекта в dev-режиме
- Установите виртуальное окружение
```
python -m venv venv
```
- Активируйте виртуальное окружение
```
source venv/Scripts/activate
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
- Выполните миграции:
```
python manage.py migrate
```
- В папке с файлом manage.py выполните команду:
```
python manage.py runserver
```
- В свем враузере введите адрес:
```
http://127.0.0.1:8000/
```
### Автор
***VanZep***
