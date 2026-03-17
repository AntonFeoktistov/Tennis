from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import DATABASE_URL
from model.base import Base

# Создаем движок
engine = create_engine(DATABASE_URL, echo=True)

# Создаем фабрику сессий
SessionLocal = sessionmaker(bind=engine, class_=Session)


def init_db():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    """Возвращает новую сессию для работы с БД"""
    return SessionLocal()


def close_session(session: Session):
    """Закрывает сессию"""
    session.close()
