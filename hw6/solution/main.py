"""
FastAPI-приложение Watchlist API.

Ниже — пример одного эндпоинта в виде заглушки.
TODO: реализуйте все эндпоинты по образцу.

Используйте декоратор @app.get / @app.post / @app.patch / @app.delete —
как на практике p5.
"""

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from solution.database import engine, get_session
from solution.models import Base

# Если используете psycopg2 вместо SQLAlchemy — импортируйте get_connection:
# from solution.database import get_connection

app = FastAPI(title="Watchlist API")

# Создаём таблицы при старте (если ещё не существуют).
# Раскомментируйте после того, как опишете модели в models.py:
# Base.metadata.create_all(bind=engine)


# ── Genres ──────────────────────────────────────────────────────────────────

@app.get("/genres", status_code=200)
def list_genres(session: Session = Depends(get_session)):
    """GET /genres -> 200, list[GenreRead]"""
    # TODO: вернуть список всех Genre
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


# POST /genres -> 201, GenreRead


# ── Movies ──────────────────────────────────────────────────────────────────

# POST   /movies        -> 201, MovieRead
# GET    /movies        -> 200, list[MovieRead]
#   query params: year (int, optional), genre_id (int, optional)
# GET    /movies/top    -> 200, list[MovieRead]
#   query params: limit (int, default=10)
#   сортировка по среднему рейтингу из reviews (DESC)
#   каждый элемент содержит avg_rating и reviews_count
# GET    /movies/{id}   -> 200, MovieRead (включает avg_rating)
# PATCH  /movies/{id}   -> 200, MovieRead
# DELETE /movies/{id}   -> 204


# ── Users ───────────────────────────────────────────────────────────────────

# POST /users           -> 201, UserRead
# GET  /users/{id}      -> 200, UserRead


# ── Reviews ─────────────────────────────────────────────────────────────────

# POST /reviews                -> 201, ReviewRead
# GET  /movies/{id}/reviews    -> 200, list[ReviewRead]


# ── Bookmarks ──────────────────────────────────────────────────────────────

# POST   /bookmarks             -> 201, BookmarkRead
# GET    /users/{id}/bookmarks  -> 200, list[BookmarkRead]
#   query params: status (str, optional: "watched" | "will_watch")
# PATCH  /bookmarks/{id}        -> 200, BookmarkRead
# DELETE /bookmarks/{id}        -> 204
