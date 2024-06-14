## Тестовое задание

#### Описание тестового задания
В данном задании нужно было создать REST API для продуктов и категорий.

Реализованные эндпоинты:
- GET /api/product/ - получение всех продуктов с фильтрами (limit, offset, name, description, price, quantity, category_id)
- GET /api/product/:id - получение информации о продукте по id
- POST /api/product/ - добавление нового продукта
- PUT /api/product/:id - изменение уже существующего продукта
- DELETE /api/product/:id - удаление существующего продукта
- GET /api/category/ - получение всех категорий
- GET /api/category/:id - получение информации о категории по id
- POST /api/category - добавление новой категории

В решении тестового задания выполнены все пункты ТЗ:
- БД - PostgreSQL, асинхронный драйвер AsyncPG с миграциями, ORM - SQLAlchemy
- Web Framework - FastAPI
- Менеджер пакетов - Poetry
- Сборка с помощью Docker Compose (команды упрощены с помощью Makefile)
- Написаны простые тесты с помощью Pytest

#### Порядок запуска
1. Клонируем репозиторий `git clone https://github.com/xorwise/tz`
2. Собираем проект `make build`
3. Запускаем проект `make run`

#### Дополнительные команды
- Остановка проекта `make stop`
- Наблюдать за проектом (логи) `make watch`
- Запуск тестов `make test`

Телеграм для связи: `@xorwise`
