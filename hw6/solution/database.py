"""
Подключение к PostgreSQL.

Вы можете выбрать ОДИН из двух подходов и реализовать всё задание на нём:

  Вариант A — SQLAlchemy ORM (рекомендуется для тех, кто хочет работать с объектами):
    Используйте engine, SessionLocal и get_session() ниже.
    Модели описывайте в models.py через DeclarativeBase.

  Вариант B — psycopg2 (raw SQL, для тех, кто хочет полный контроль над запросами):
    Используйте get_connection() ниже.
    Запросы пишите SQL-строками с плейсхолдерами %s.

Файл можно менять как угодно.
"""

import os

import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Локально (после createuser -s): postgresql+psycopg2:///watchlist
# Если нужен пароль: postgresql+psycopg2://postgres:postgres@localhost:5432/watchlist
# В CI (GitHub Actions) переменная DATABASE_URL выставлена автоматически.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2:///watchlist",
)

# ── Вариант A: SQLAlchemy ORM ────────────────────────────────────────────────

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_session():
    """FastAPI Dependency: выдаёт SQLAlchemy-сессию."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# ── Вариант B: psycopg2 (raw SQL) ────────────────────────────────────────────

# DSN для psycopg2 (берём из DATABASE_URL, убирая +psycopg2 из схемы)
_PG_DSN = DATABASE_URL.replace("postgresql+psycopg2", "postgresql")


def get_connection():
    """FastAPI Dependency: выдаёт psycopg2-соединение с RealDictCursor."""
    conn = psycopg2.connect(_PG_DSN, cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
