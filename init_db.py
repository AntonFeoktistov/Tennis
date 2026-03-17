import sys
import os

# Добавляем корень проекта в путь (чтобы импорты работали)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.db import engine, Base
from model.player import Player
from model.match import Match


def init_database():
    """Создает все таблицы в базе данных"""
    print("Создание таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)
    print("✅ База данных успешно создана!")


if __name__ == "__main__":
    init_database()
