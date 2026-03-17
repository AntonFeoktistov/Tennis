from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Session


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass
