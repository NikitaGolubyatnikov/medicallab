import mysql.connector
from mysql.connector import Error
from core.config import Config
import logging
import bcrypt


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            logger.info("🛠 Подключение к базе данных...")
            self.connection = mysql.connector.connect(**Config.DB_CONFIG)
            logger.info("✅ Подключение успешно")
        except Error as e:
            logger.error(f"❗ Ошибка подключения к базе данных: {e}")
            self.connection = None

    def get_user(self, login: str):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        if not self.connection:
            logger.error("❗ Нет соединения с БД при попытке получить пользователя.")
            return None

        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE login = %s", (login,))
        return cursor.fetchone()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def get_all_users(self):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, login, full_name, role, last_login FROM users WHERE is_archived IS NULL OR is_archived = 0")
        return cursor.fetchall()

    def update_user(self, user_id, login, full_name, role):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE users
            SET login = %s, full_name = %s, role = %s
            WHERE id = %s
        """, (login, full_name, role, user_id))
        self.connection.commit()

    def add_user(self, login, password, full_name, role):
        if self.connection is None or not self.connection.is_connected():
            self.connect()

        try:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            cursor = self.connection.cursor()
            cursor.execute(
                """
                INSERT INTO users (login, password_hash, full_name, role)
                VALUES (%s, %s, %s, %s)
                """,
                (login, hashed, full_name, role)
            )
            self.connection.commit()
            return True

        except Exception as e:
            print("❌ Ошибка при добавлении пользователя:", e)
            return False

    def update_last_login(self, user_id):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE users
            SET last_login = NOW()
            WHERE id = %s
        """, (user_id,))
        self.connection.commit()

    def archive_user(self, user_id):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE users
            SET is_archived = 1
            WHERE id = %s
        """, (user_id,))
        self.connection.commit()

    def get_users(self, archived=False):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor(dictionary=True)
        if archived:
            cursor.execute("SELECT id, login, full_name, role, last_login FROM users WHERE is_archived = 1")
        else:
            cursor.execute(
                "SELECT id, login, full_name, role, last_login FROM users WHERE is_archived IS NULL OR is_archived = 0")
        return cursor.fetchall()

    def restore_user(self, user_id):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE users
            SET is_archived = 0
            WHERE id = %s
        """, (user_id,))
        self.connection.commit()

    def add_patient(self, full_name, date_of_birth, passport_series_number, phone, email, insurance_number, insurance_type):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO patients (full_name, date_of_birth, passport_series_number, phone, email, insurance_number, insurance_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (full_name, date_of_birth, passport_series_number, phone, email, insurance_number, insurance_type))
        self.connection.commit()

    def get_patients(self, archived=False):
        with self.connection.cursor(dictionary=True) as cursor:
            if archived:
                cursor.execute("SELECT * FROM patients WHERE is_archived = 1")
            else:
                cursor.execute("SELECT * FROM patients WHERE is_archived = 0 OR is_archived IS NULL")
            return cursor.fetchall()

    def get_patient_by_id(self, patient_id):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
            return cursor.fetchone()

    def get_all_patients(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id, full_name FROM patients WHERE is_archived = 0")
            return cursor.fetchall()

    def get_tube_codes(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT DISTINCT tube_code FROM orders")
            return [row['tube_code'] for row in cursor.fetchall()]

    def get_all_services(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT code, name, cost FROM services")
            return [(row['code'], row['name'], row['cost']) for row in cursor.fetchall()]

    def get_services_for_dropdown(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT code, name FROM services")
            return cursor.fetchall()

    def find_services(self, search_term):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT code, name, cost FROM services WHERE LOWER(name) LIKE %s LIMIT 10",
                (f"%{search_term.lower()}%",)
            )
            return cursor.fetchall()

    def is_tube_code_exists(self, code):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as cnt FROM orders WHERE tube_code = %s", (code,))
            return cursor.fetchone()['cnt'] > 0

    def create_order(self, patient_id, tube_code, services):
        with self.connection.cursor(dictionary=True) as cursor:
            if not tube_code:
                cursor.execute("SELECT COUNT(*) as c FROM orders")
                tube_code = f"TUBE-{cursor.fetchone()['c'] + 1:04d}"

            cursor.execute(
                "INSERT INTO orders (patient_id, tube_code) VALUES (%s, %s)",
                (patient_id, tube_code)
            )
            order_id = cursor.lastrowid
            for code in services:
                cursor.execute(
                    "INSERT INTO order_services (order_id, service_id) SELECT %s, id FROM services WHERE code = %s",
                    (order_id, code)
                )
            self.connection.commit()

            return order_id

    def get_order_by_id(self, order_id):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            return cursor.fetchone()

    def get_patient_by_id(self, patient_id):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
            return cursor.fetchone()

    def get_order_services(self, order_id):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT s.name, s.cost FROM services s
                JOIN order_services os ON s.id = os.service_id
                WHERE os.order_id = %s
            """, (order_id,))
            return cursor.fetchall()

    def log_login_attempt(self, login: str, success: bool):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO login_logs (login, success) VALUES (%s, %s)
        """, (login, success))
        self.connection.commit()

    def get_login_logs(self, login_filter=None):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor(dictionary=True)
        if login_filter:
            cursor.execute(
                "SELECT * FROM login_logs WHERE login LIKE %s ORDER BY attempt_time DESC",
                (f"%{login_filter}%",)
            )
        else:
            cursor.execute("SELECT * FROM login_logs ORDER BY attempt_time DESC")
        return cursor.fetchall()

    def get_all_orders(self, archived=False):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders WHERE archived = %s ORDER BY created_at DESC", (archived,))
        return cursor.fetchall()

    def archive_order(self, order_id):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute("UPDATE orders SET archived = 1 WHERE id = %s", (order_id,))
        self.connection.commit()

    def restore_order(self, order_id):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute("UPDATE orders SET archived = 0 WHERE id = %s", (order_id,))
        self.connection.commit()

    def set_patient_archive(self, patient_id: int, archive: bool):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE patients SET is_archived = %s WHERE id = %s",
            (1 if archive else 0, patient_id)
        )
        self.connection.commit()












