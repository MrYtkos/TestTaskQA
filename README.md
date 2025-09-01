# TestTaskQA

API-сервес на Django REST Framework с PostgreSQL и Docker.

---


---
## Для запуска нужен
- Docker + docker-compose
---
## Запуск проекта
1. **Клонировать репозиторий**
````bash
git clone <URL_REPO>
cd TestTaskQA
````
2. **Создать файл .env (для переменных окружения):**

POSTGRES_DB=testtaskqa

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres 

POSTGRES_HOST=db 

POSTGRES_PORT=5432

3. **Запустить Docker и собрать контйнер**
````bash
docker-compose up --build
````
4. **API будет доступен по адресу: http://localhost:8000/api/**

## **Запуск тестов**
Можно через docker
````bash
docker-compose run web pytest
````

## Методы API
1. Вопросы (Questions):
- GET /questions/ - список всех вопросов
- POST /questions/ - создать новый вопрос
- GET /questions/{id} - получить вопрос и все ответы на него
- DELETE /questions/{id} - удалить вопрос (вместе с ответами)
2. Ответы(Answers):
- GET /answers/{id} - получить конкретный ответ
- DELETE /answers/{id} - удалить ответ
- POST /questions/{id}/answers/ - добавить ответ к вопросу

## Логика
- Нельзя создать ответ к несуществующему вопросу.
- Один и тот же пользователь может оставлять несколько ответов на один вопрос.
- При удалении вопроса должны удаляться все его ответы (каскадно).