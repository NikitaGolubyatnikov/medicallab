# 📂 Файл: auth/login_window.py

import sys
import logging
import bcrypt
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal, Qt, QTimer

from bd.database import Database
from auth.captcha import CaptchaGenerator
from core.session import SessionManager
from core.config import Config
from ui.admin_panel import AdminPanel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoginWindow(QWidget):
    login_success = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        logger.info("1: Начало LoginWindow.__init__()")

        self.db = Database()
        logger.info("2: Инициализация Database()...")

        self.session = SessionManager()
        logger.info("3: Инициализация SessionManager()...")

        self.captcha_generator = CaptchaGenerator()
        logger.info("4: Инициализация CaptchaGenerator()...")

        self.failed_attempts = 0
        self.current_captcha_text = ""

        self.setup_ui()
        logger.info("5: Setup UI...")

        self.setup_connections()
        logger.info("6: Setup Connections...")

        self.refresh_captcha()
        logger.info("7: Refresh Captcha...")

        self.captcha_image.hide()
        self.captcha_input.hide()
        self.refresh_captcha_btn.hide()
        self.session_timer = QTimer()
        self.session_timer.setInterval(60 * 1000)  # проверка каждую минуту
        self.session_time_left = 10  # 10 минут
        self.session_timer.timeout.connect(self.update_session_timer)

        logger.info("8: LoginWindow.__init__() завершён")

    def setup_ui(self):
        self.setWindowTitle("Авторизация")
        self.setFixedSize(480, 440)

        main_layout = QVBoxLayout()

        main_layout = QVBoxLayout()

        # Логотип
        DIR = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.normpath(os.path.join(DIR, "..", "resources", "XXL_height.webp"))
        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pix = QPixmap(logo_path)
        if not pix.isNull():
            logo.setPixmap(pix.scaled(328, 328, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            logo.setText("⚠ Нет логотипа")
        main_layout.addWidget(logo)

        # Заголовок
        self.title_label = QLabel("Медицинская Лаборатория")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.title_label)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        main_layout.addWidget(self.login_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.show_password_btn = QPushButton("👁")
        self.show_password_btn.setCheckable(True)
        self.show_password_btn.setFixedWidth(40)

        pass_layout = QHBoxLayout()
        pass_layout.addWidget(self.password_input)
        pass_layout.addWidget(self.show_password_btn)
        main_layout.addLayout(pass_layout)

        self.captcha_image = QLabel()
        self.captcha_image.setFixedHeight(60)
        self.captcha_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.captcha_image)

        self.captcha_input = QLineEdit()
        self.captcha_input.setPlaceholderText("Введите капчу")
        main_layout.addWidget(self.captcha_input)

        self.refresh_captcha_btn = QPushButton("Обновить капчу")
        main_layout.addWidget(self.refresh_captcha_btn)

        self.login_btn = QPushButton("Войти")
        main_layout.addWidget(self.login_btn)

        self.setLayout(main_layout)

    def setup_connections(self):
        self.show_password_btn.toggled.connect(self.toggle_password_visibility)
        self.refresh_captcha_btn.clicked.connect(self.refresh_captcha)
        self.login_btn.clicked.connect(self.handle_login)

    def toggle_password_visibility(self, checked):
        self.password_input.setEchoMode(QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password)
        self.show_password_btn.setText("🙈" if checked else "👁")

    def refresh_captcha(self):
        try:
            captcha = self.captcha_generator.generate()
            pixmap = QPixmap()
            pixmap.loadFromData(captcha, 'PNG')
            self.captcha_image.setPixmap(pixmap)
            self.current_captcha_text = self.captcha_generator.get_last_text()
            self.captcha_input.clear()
            logger.info(f"CAPTCHA сгенерирована: {self.current_captcha_text}")
        except Exception as e:
            logger.error(f"Ошибка генерации CAPTCHA: {e}")
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить капчу")

    def validate_captcha(self):
        return self.captcha_input.text().strip().lower() == self.current_captcha_text.lower()

    def handle_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not login or not password:
            self.show_error('Заполните все поля!')
            return

        if self.failed_attempts >= 3:
            if not self.validate_captcha():
                self.show_error('Неверная капча.')
                self.refresh_captcha()
                return

        try:
            user = self.db.get_user(login)
            if not user:
                self.db.log_login_attempt(login, False)
                self.failed_login()
                return

            print("🧪 DEBUG: Введённый логин:", repr(login))
            print("🧪 DEBUG: Введённый пароль:", repr(password))
            print("🧪 DEBUG: Полученный user из БД:", user)

            stored_hash = user.get("password_hash") or user.get("password hash")
            print("🧪 DEBUG: Хэш из БД:", repr(stored_hash))

            if stored_hash:
                try:
                    check = bcrypt.checkpw(password.encode(), stored_hash.encode())
                    print("🧪 DEBUG: Сравнение:", check)
                    if check:
                        self.db.log_login_attempt(login, True)
                        self.handle_success_login(user)
                        return
                except Exception as e:
                    print("🛑 ERROR при bcrypt.checkpw():", e)

            self.db.log_login_attempt(login, False)
            self.failed_login()

        except Exception as e:
            logger.error(f"Ошибка авторизации: {e}")
            self.db.log_login_attempt(login, False)
            self.failed_login()

    def failed_login(self):
        self.failed_attempts += 1

        if self.failed_attempts >= Config.MAX_LOGIN_ATTEMPTS:
            self.captcha_image.show()
            self.captcha_input.show()
            self.refresh_captcha_btn.show()
            self.session.block()
            QTimer.singleShot(Config.BLOCK_TIME * 1000, self.reset_block)

        QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
        self.refresh_captcha()

    def handle_success_login(self, user_data):
        try:
            self.db.update_last_login(user_data['id'])
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить дату входа: {e}")

        role = user_data['role']

        if role == 'admin':
            from ui.admin_panel import AdminPanel
            self.admin_panel = AdminPanel()
            self.admin_panel.show()

        elif role == 'lab_assistant':
            from ui.lab_assistant_panel import LabAssistantPanel
            self.lab_panel = LabAssistantPanel()
            self.lab_panel.show()

        elif role == 'researcher':
            from ui.research_assistant_panel import ResearchAssistantPanel
            self.research_panel = ResearchAssistantPanel()
            self.research_panel.show()

        elif role == 'accountant':
            from ui.accountant_panel import AccountantPanel
            self.accountant_panel = AccountantPanel()
            self.accountant_panel.show()

        else:
            QMessageBox.warning(self, "Ошибка", f"Неизвестная роль: {role}")
            return

        QMessageBox.information(self, "Успех", "Успешный вход!")

        self.session_timer.stop()  # Остановить таймер обязательно!
        self.close()  # Закрыть LoginWindow

    def reset_block(self):
        self.failed_attempts = 0
        self.session.unblock()
        self.refresh_captcha()

    def show_error(self, message):
        QMessageBox.warning(self, "Ошибка", message)

    def update_session_timer(self):
        self.session_time_left -= 1

        if self.session_time_left == 5:
            QMessageBox.warning(self, "Предупреждение", "Через 5 минут сеанс завершится.")

        if self.session_time_left <= 0:
            self.session_timer.stop()
            self.session.block()
            QMessageBox.information(self, "Сеанс завершён",
                                    "Время сеанса истекло. Повторный вход возможен через 1 минуту.")
            self.logout_and_lock()
        if hasattr(self, 'admin_panel'):
            self.admin_panel.session_time_label.setText(f"Осталось: {self.session_time_left:02d}:00")

    def logout_and_lock(self):
        self.login_input.clear()
        self.password_input.clear()
        self.captcha_input.clear()

        self.captcha_image.hide()
        self.captcha_input.hide()
        self.refresh_captcha_btn.hide()

        # Закрыть активную панель, если есть
        if hasattr(self, 'admin_panel'):
            self.admin_panel.close()

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())