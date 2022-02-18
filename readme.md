### Небольшой аналог платформы SoundCloud

#### Инструменты разработки

<span>`Django`</span>
<span>`DjangoRestFramework`</span>


#### Установка:

1. Создайте виртуальное окружение и активируйте его `python -m venv venv` и `source venv/bin/activate`
2. Скачайте репозиторий `https://github.com/Untouchable17/Blackout-Sound.git`
3. Установите все зависимости `pip install -r requirements.txt`
5. Создайте миграции в базе данных `python manage.py makemigrations`
6. Примените созданные миграции `python manage.py migrate`
7. Создайте суперпользователя `python manage.py createsuperuser`
=======

### Запуск в продакшн

1. В файле `.prod_env` заполните все необходимые поля
2. Создайте образ и запустите контейнер `docker-compose up --build`
3. Создайте суперпользователя:<br><br>
   `docker exec -it blackout_sound_web bash`<br>
   `python manage.py createsuperuser`

