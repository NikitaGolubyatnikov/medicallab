# 📂 Файл: bd/import_data.py

import csv
import bcrypt
import mysql.connector
from core.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROLE_MAPPING = {
    '1': 'lab_assistant',
    '2': 'researcher',
    '3': 'accountant',
    '4': 'admin'
}


def import_users(cursor):
    with open('users.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                role = ROLE_MAPPING.get(row['type'], 'lab_assistant')
                password_plain = row['password']
                password_hashed = bcrypt.hashpw(password_plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                cursor.execute("""
                    INSERT INTO users (login, password_hash, full_name, role)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        full_name = VALUES(full_name),
                        role = VALUES(role)
                """, (row['login'], password_hashed, row['name'], role))
                logger.info(f"✅ Пользователь добавлен/обновлён: {row['login']}")
            except Exception as e:
                logger.error(f"❗ Ошибка добавления пользователя {row.get('login', 'Unknown')}: {e}")


def import_services(cursor):
    with open('services.csv', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                code = row.get('Code')
                name = row.get('Service')
                price = row.get('Price')

                if not (code and name and price):
                    logger.warning(f"❗ Пропущена строка из-за отсутствия данных: {row}")
                    continue

                cursor.execute("""
                    INSERT INTO services (code, name, cost, result_type, available_analyzers)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        name = VALUES(name),
                        cost = VALUES(cost)
                """, (code, name, price, 'Integer', 'Ledetect | Biorad'))
                logger.info(f"✅ Услуга добавлена/обновлена: {name}")
            except Exception as e:
                logger.error(f"❗ Ошибка добавления услуги {row.get('Service', 'Unknown')}: {e}")


def main():
    try:
        connection = mysql.connector.connect(**Config.DB_CONFIG)
        cursor = connection.cursor()

        import_users(cursor)
        import_services(cursor)

        connection.commit()
        logger.info("🎉 Импорт завершён успешно!")

    except mysql.connector.Error as e:
        logger.error(f"❗ Ошибка подключения к БД: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == '__main__':
    main()
