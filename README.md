# Структура
В проекте два сервиса Users и Offers, каждый в своей папке.

# Запуск

#### virtualenv
> ```bash
> $ python3 -m pip install virtualenv
> $ virtualenv venv
> $ source venv/bin/activate
> ```

#### requirements
>```bash
> (venv) $ pip install -r requirements.txt
>```

#### настройки

Прописать данные для подключения к БД в .env

#### старт
> ```bash
> (venv) $ python main.py
> ```


#### Альтернативный старт Docker
> ```bash
> $ sudo docker-compose -f docker-compose.yml up -d --build
> ```
