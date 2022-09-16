# Проект: запуск docker-compose
## Описание проекта
Результаты тестовых заданий для Python-разработчиков часто просят отправлять в контейнерах. Это делается для того, чтобы человеку, который будет проверять ваше тестовое, не пришлось настраивать окружение на своём компьютере. В этом финальном проекте ревьюер сыграет роль работодателя, а проект api_yamdb будет результатом вашего тестового задания. Ваша задача — отправить проект «работодателю» «вместе с компьютером» — в контейнере.
## Стек технологий
Django, gunicorn, nginx, docker, REST API
## Запуск проекта через Docker
Собрать контейнер:
 -   docker-compose up -d --build

Выполнить следующие команды:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
docker-compose exec web python manage.py loaddata fixtures.json
```
## Запуск проекта в dev-режиме
-   Установить и активировать виртуальное окружение
-   Установить зависимости из файла requirements.txt
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
-   Выполнить миграции:
```
python manage.py migrate
```
-   В папке с файлом manage.py выполнить команду:
```
python manage.py runserver
```
-   Для загрузки тестовых данных из csv-файлов выполнить команду:
```
python manage.py load_data
```
### Работа с API для всех пользователей

Для неавторизованных пользователей работа с API доступна только в режиме чтения
```
GET /api/v1/categories/ - Получение списка всех категорий
GET /api/v1/genres/ - Получение списка всех жанров
GET /api/v1/titles/ - Получение списка всех произведений
GET /api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву
```
### Работа с API для авторизованных пользователей

Получение данных своей учетной записи:
```
Права доступа: user
GET api/v1/users/me/
```
Добавление категорий:
```
Права доступа: admin
POST /api/v1/categories/

{
  "name": "string",
  "slug": "string"
}
```
Добавление жанров:
```
Права доступа: admin
POST /api/v1/genres/

{
  "name": "string",
  "slug": "string"
}
```
Добавление произведений и обновление информации о произведении:
```
Права доступа: admin
POST /api/v1/titles/
PATCH /api/v1/titles/{titles_id}/

{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
## Автор
Студент Хайдаров Руслан
