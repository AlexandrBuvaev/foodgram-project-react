# praktikum_new_diplom
**Установка проекта**
- Клонирование репозитория:
```bash
git@github.com:AlexandrBuvaev/foodgram-project-react.git
```
**Создайте файл .env по образцу env_example.txt в директории .infra/: **
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
sudo docker compose exec web python manage.py migrate
sudo docker compose exec web python manage.py createsuperuser
sudo docker compose exec web python manage.py collectstatic --no-input
```
**Для закрытия контейнера используйте команду:**
```bash
sudo docker-compose down -v
```