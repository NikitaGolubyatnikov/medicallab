# 📂 Файл: core/config.py

class Config:
    # Настройки базы данных
    DB_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "eggo",
        "database": "medicallab",
        "port": 3306
    }

    # Настройки авторизации
    MAX_LOGIN_ATTEMPTS = 3
    BLOCK_TIME = 60  # Время блокировки в секундах
