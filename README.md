# Проект: запуск docker-compose
## Описание проекта
Результаты тестовых заданий для Python-разработчиков часто просят отправлять в контейнерах. Это делается для того, чтобы человеку, который будет проверять ваше тестовое, не пришлось настраивать окружение на своём компьютере. В этом финальном проекте ревьюер сыграет роль работодателя, а проект api_yamdb будет результатом вашего тестового задания. Ваша задача — отправить проект «работодателю» «вместе с компьютером» — в контейнере.
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
