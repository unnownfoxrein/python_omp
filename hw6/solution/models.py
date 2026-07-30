"""
SQLAlchemy-модели для базы watchlist.

Таблицы:
  - genres     жанры
  - movies     фильмы (FK -> genres)
  - users      пользователи
  - reviews    отзывы (FK -> users, movies; UNIQUE user+movie)
  - bookmarks  закладки (FK -> users, movies; UNIQUE user+movie)

TODO: опишите модели.
      Подсказка — вы уже делали похожее на практике p7.
      Главное отличие: поле watched убрано из movies,
      вместо него — отдельная таблица bookmarks (per-user).
"""

from solution.database import Base  # noqa: F401

# TODO: импорты из sqlalchemy

# TODO: модель Genre

# TODO: модель Movie (без поля watched!)

# TODO: модель User

# TODO: модель Review (UNIQUE user_id + movie_id)

# TODO: модель Bookmark
#   user_id   FK -> users
#   movie_id  FK -> movies
#   status    строка: "watched" или "will_watch"
#   UNIQUE(user_id, movie_id)
