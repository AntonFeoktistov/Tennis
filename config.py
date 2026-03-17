import os

# Настройки базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tennis.db")

# Другие настройки приложения
DEBUG = True
SECRET_KEY = "your-secret-key"
