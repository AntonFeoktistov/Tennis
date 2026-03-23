from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import Config
from model.base import Base

engine = create_engine(Config.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=Session)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    return SessionLocal()


def close_session(session: Session):
    session.close()
