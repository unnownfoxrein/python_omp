# Домашнее задание №6 — Watchlist API

### Как сдавать решения?

1. Склонировать репозиторий

2. Создать виртуальное окружение и установить зависимости:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Сделать ветку `dev`: `git checkout -b dev`. Решать задание нужно в этой ветке. Все файлы для редактирования находятся в папке `solution`.

4. Как только вы готовы отправить решение — откройте Pull Request в ветку `main` и добавьте преподавателя в Reviewers. Название PR: `HW6. Фамилия Имя`.


### Подготовка PostgreSQL

Вам нужна работающая PostgreSQL и база `watchlist`. Если вы уже настроили PostgreSQL на практиках p6/p7 — просто создайте новую базу (шаг 2).

#### macOS

```bash
# 1. Установить и запустить (если еще не сделали на практике)
brew install postgresql@16
brew services start postgresql@16

# Создать суперпользователя с вашим логином (если еще нет)
createuser -s $(whoami) 2>/dev/null || true

# 2. Создать базу данных
createdb watchlist

# 3. Проверить, что все работает
psql -d watchlist -c "SELECT version();"
```

После этого в `solution/database.py` строка подключения без пароля:
```
postgresql+psycopg2:///watchlist
```

#### Linux / Windows (WSL)

```bash
# 1. Установить и запустить (если еще не сделали на практике)
sudo apt update && sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable --now postgresql

# Создать суперпользователя с вашим логином (если еще нет)
sudo -u postgres createuser -s $USER 2>/dev/null || true

# 2. Создать базу данных
createdb watchlist

# 3. Проверить, что все работает
psql -d watchlist -c "SELECT version();"
```

После этого в `solution/database.py` строка подключения без пароля:
```
postgresql+psycopg2:///watchlist
```

> **Если `createdb` / `psql` не работает без `-U postgres`**, значит суперпользователь не создался. Тогда используйте:
> ```bash
> sudo -u postgres createdb watchlist
> ```
> и в `database.py`:
> ```
> postgresql+psycopg2://postgres:postgres@localhost:5432/watchlist
> ```


### Как запустить сервер и тесты

1. Запустить сервер:

```bash
make run
# или
uvicorn solution.main:app --reload
```

2. В другом терминале запустить тесты:

```bash
make test
# или
pytest test -s
```

3. Линтеры и форматтер:

```bash
make fmt lint
```

> **CI:** В GitHub Actions PostgreSQL поднимается автоматически. Менять ничего не нужно — просто открывайте PR и смотрите результат.


---


## Задание

Вам нужно реализовать REST API для сервиса **Watchlist** — персонального трекера фильмов.


### Выбор подхода к БД

Вы можете выбрать **один** из двух вариантов и реализовать все задание на нем.
Тесты проверяют HTTP-интерфейс — им неважно, как вы работаете с БД внутри.

| | Вариант A: SQLAlchemy ORM | Вариант B: psycopg2 (raw SQL) |
|--|--------------------------|-------------------------------|
| **Когда** | хотите работать с Python-объектами | хотите писать SQL напрямую |
| **Модели** | описываете классы в `models.py` | таблицы создаете SQL-скриптом |
| **Запросы** | `session.query(Movie).filter(...)` | `cur.execute("SELECT ...", (…,))` |
| **Dependency** | `get_session()` из `database.py` | `get_connection()` из `database.py` |
| **Практика** | p7 (SQLAlchemy) | p6 (psycopg2) |

Оба варианта уже подготовлены в `solution/database.py` — выберите нужный и используйте.

Пользователь может:
- Просматривать каталог фильмов по жанрам
- Оставлять отзывы с рейтингом
- Добавлять фильмы в закладки (хочу посмотреть / уже посмотрел)
- Смотреть топ фильмов по среднему рейтингу


### Схема БД

```
genres:     id, name (UNIQUE)
movies:     id, title, year, genre_id (FK -> genres), created_at
users:      id, username (UNIQUE), email (UNIQUE)
reviews:    id, user_id (FK), movie_id (FK), rating (1-10), comment, created_at
            UNIQUE(user_id, movie_id) — один отзыв на фильм от одного пользователя
bookmarks:  id, user_id (FK), movie_id (FK), status ("watched" | "will_watch"), created_at
            UNIQUE(user_id, movie_id)
```

**Важно:** на практике p7 у нас было поле `watched` прямо в таблице `movies`. Подумайте, почему это неправильно, если у нас есть таблица `users`. В этом задании `watched` — это per-user состояние через отдельную таблицу `bookmarks`.


### Что реализовать

Все файлы находятся в `solution/`:

| Файл | Что нужно сделать |
|------|------------------|
| `models.py` | Описать SQLAlchemy-модели: Genre, Movie, User, Review, Bookmark |
| `schemas.py` | Описать Pydantic-схемы для валидации запросов и ответов |
| `main.py` | Реализовать FastAPI-эндпоинты (список ниже) |
| `database.py` | Можно менять (и, возможно, придется) |


### Эндпоинты

#### Genres (5 баллов)

| Метод | URL | Код | Описание |
|-------|-----|-----|----------|
| POST | `/genres` | 201 | Создать жанр |
| GET | `/genres` | 200 | Список всех жанров |

#### Movies (20 баллов)

| Метод | URL | Код | Описание |
|-------|-----|-----|----------|
| POST | `/movies` | 201 | Создать фильм |
| GET | `/movies` | 200 | Список фильмов. Query params: `year`, `genre_id` (оба опциональные) |
| GET | `/movies/top` | 200 | Топ фильмов по среднему рейтингу. Query: `limit` (default 10). Каждый элемент содержит `avg_rating` и `reviews_count` |
| GET | `/movies/{id}` | 200 | Один фильм. Содержит `avg_rating` (среднее из reviews) |
| PATCH | `/movies/{id}` | 200 | Обновить фильм (частичное обновление) |
| DELETE | `/movies/{id}` | 204 | Удалить фильм (с каскадным удалением отзывов и закладок) |

#### Users (5 баллов)

| Метод | URL | Код | Описание |
|-------|-----|-----|----------|
| POST | `/users` | 201 | Создать пользователя |
| GET | `/users/{id}` | 200 | Получить пользователя |

#### Reviews (15 баллов)

| Метод | URL | Код | Описание |
|-------|-----|-----|----------|
| POST | `/reviews` | 201 | Создать отзыв. `rating` от 1 до 10 |
| GET | `/movies/{id}/reviews` | 200 | Все отзывы фильма |

#### Bookmarks (15 баллов)

| Метод | URL | Код | Описание |
|-------|-----|-----|----------|
| POST | `/bookmarks` | 201 | Добавить в закладки. `status`: `"watched"` или `"will_watch"` |
| GET | `/users/{id}/bookmarks` | 200 | Закладки пользователя. Query: `status` (опционально) |
| PATCH | `/bookmarks/{id}` | 200 | Обновить статус закладки |
| DELETE | `/bookmarks/{id}` | 204 | Удалить закладку |


### Обработка ошибок (10 баллов)

| Ситуация | HTTP-код |
|----------|---------|
| Невалидные данные (Pydantic) | 422 |
| Ссылка на несуществующую сущность (FK) | 400 или 404 |
| Дубликат (UNIQUE violation) | 409 |
| Сущность не найдена | 404 |

**Важно:** сервер **никогда** не должен возвращать 500. Ловите `IntegrityError` от SQLAlchemy и возвращайте корректные HTTP-коды.


### Нагрузочный тест (15 баллов)

Тесты `test_performance.py` отправляют **100 параллельных** HTTP-запросов к вашему серверу. Все запросы должны завершиться менее чем за **2 секунды**.

Если тест не проходит — читайте сообщение об ошибке, там есть подсказка.


### Баллы

| Категория | Баллов |
|-----------|--------|
| Genres | 5 |
| Movies (CRUD + фильтры) | 20 |
| Users | 5 |
| Reviews + avg_rating + top | 15 |
| Bookmarks | 15 |
| Constraints (FK, UNIQUE, CHECK → не 500) | 10 |
| Movies top (raw SQL) | 5 |
| avg_rating в GET /movies/{id} | 5 |
| Нагрузочный тест | 15 |
| Линтер (ruff) | 5 |
| **Итого** | **100** |



### Полезные ссылки

- [FastAPI — Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- [FastAPI — Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [FastAPI — Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [SQLAlchemy ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [Pydantic v2 — Models](https://docs.pydantic.dev/latest/concepts/models/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
