**Foodgram - продуктовый помощник**
![foodgram_back-app workflow](https://github.com/AlexandrBuvaev/foodgram-project-react/actions/workflows/foodgram_back_workflow.yaml/badge.svg)

Дипломный проект в рамках Яндекс Практикума. Онлайн-сервис на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в "Избранное", а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
Протестировать функционал сервиса можно по адресу:  http://158.160.45.105/

**Учетные данные для тестирования админки доступной по адресу http://158.160.45.105/admin**
```bash
login: admin@mail.ru
password: admin123
```

**Установка проекта**
- Клонирование репозитория:
```bash
git@github.com:AlexandrBuvaev/foodgram-project-react.git
```
**Создайте файл .env по образцу env_example.txt в директории .infra/:**
```
DB_NAME=<db_name>
POSTGRES_USER=<pg_username>
POSTGRES_PASSWORD=<pg_password>
DB_HOST=<localhost>
DB_PORT=<5432>
```
**Запуск docker-compose.yaml:**
```bash
sudo docker compose up -d --build
```
**Создание миграций, сборка статики и создание суперпользователя.**
```bash
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py createsuperuser
sudo docker compose exec backend python manage.py collectstatic --no-input
```
**Опционально можно загрузить тестовые данные для ингридиентов и тегов.**
```bash
sudo docker compose exec backend python3 manage.py load_ingrs
sudo docker compose exec backend python3 manage.py load_tags
```
**Для закрытия контейнера используйте команду:**
```bash
sudo docker-compose down -v
```