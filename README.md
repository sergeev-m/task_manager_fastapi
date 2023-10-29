# Task Manager

Диспетчер задач реального времени с использованием FastAPI. API позволит пользователям управлять
своими задачами, создавать новые задачи, помечать их как выполненные и удалять задачи. Кроме того,
пользователи будут получать обновления в режиме реального времени всякий раз, когда меняется статус
задачи.

## Старт

```bash
git clone git@github.com:sergeev-m/task_manager_fastapi.git

# Переименовать .env.example на .env

docker-compose up
```

## Документация: 
http://127.0.0.1:8000/api/v1/docs


## Используемы инструменты

- python - 3.12
- fastapi - 0.104.0
- sqlalchemy - 2.0.22
- postgres - 15
- docker compose - 3.9

***

### Контакты

Михаил  
[email](server-15@yandex.ru)  
[telegram](https://t.me/sergeev_mikhail)
