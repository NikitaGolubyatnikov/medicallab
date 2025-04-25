# 📂 Файл: ui/admin_panel.py
from PyQt6.QtWidgets import (
    QApplication, QMessageBox, QMainWindow, QLabel, QVBoxLayout, QWidget,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLineEdit,
    QHBoxLayout, QComboBox, QMenu
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, QEvent
from ui.order_panel import OrderPanel
from ui.patient_panel import PatientPanel
from bd.database import Database
import os

class AddUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавление пользователя")
        self.setFixedSize(400, 350)

        layout = QVBoxLayout()

        self.login_input = QLineEdit()
        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_input)


        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)

        self.full_name_input = QLineEdit()
        layout.addWidget(QLabel("ФИО:"))
        layout.addWidget(self.full_name_input)

        self.role_input = QComboBox()
        self.role_input.addItems(["admin", "researcher", "lab_assistant", "accountant"])
        layout.addWidget(QLabel("Роль:"))
        layout.addWidget(self.role_input)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.save_button.clicked.connect(self.save_user)
        self.cancel_button.clicked.connect(self.close)

    def save_user(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()
        full_name = self.full_name_input.text().strip()
        role = self.role_input.currentText()

        if not login or not password or not full_name:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        try:
            db = Database()
            db.add_user(login, password, full_name, role)  # <--- только чистый пароль!
            QMessageBox.information(self, "Успех", "Пользователь добавлен успешно!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить пользователя: {e}")


class EditUserDialog(QDialog):
    def __init__(self, user_id, login, full_name, role):
        super().__init__()
        self.setWindowTitle("Редактирование пользователя")
        self.setFixedSize(400, 300)

        self.user_id = user_id

        layout = QVBoxLayout()

        self.login_input = QLineEdit()
        self.login_input.setText(login)
        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_input)

        self.full_name_input = QLineEdit()
        self.full_name_input.setText(full_name)
        layout.addWidget(QLabel("ФИО:"))
        layout.addWidget(self.full_name_input)

        self.role_input = QComboBox()
        self.role_input.addItems(["admin", "researcher", "lab_assistant", "accountant"])
        self.role_input.setCurrentText(role)
        layout.addWidget(QLabel("Роль:"))
        layout.addWidget(self.role_input)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.save_button.clicked.connect(self.save_user)
        self.cancel_button.clicked.connect(self.close)

    def save_user(self):
        new_login = self.login_input.text().strip()
        new_full_name = self.full_name_input.text().strip()
        new_role = self.role_input.currentText()

        try:
            db = Database()
            db.update_user(self.user_id, new_login, new_full_name, new_role)
            QMessageBox.information(self, "Успех", "Пользователь обновлён успешно!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить пользователя: {e}")

class AdminPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель Администратора")
        self.setGeometry(100, 100, 1000, 700)

        self.db = Database()

        self.showing_archive = False

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # --- Верхняя строка: аватар справа ---
        top_bar = QHBoxLayout()
        self.title_label = QLabel("Добро пожаловать в панель администратора!")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        DIR = os.path.dirname(os.path.abspath(__file__))
        avatar_path = os.path.normpath(os.path.join(DIR, "..", "resources", "administrator.png"))
        self.avatar = QLabel()
        self.avatar.setFixedSize(164, 164)
        pix = QPixmap(avatar_path)
        if not pix.isNull():
            self.avatar.setPixmap(pix.scaled(164, 164, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.avatar.setText("⚠")

        top_bar.addWidget(self.title_label)
        top_bar.addStretch()
        top_bar.addWidget(self.avatar)

        layout.addLayout(top_bar)

        self.session_time_left = 600
        self.session_timer = QTimer(self)
        self.session_timer.timeout.connect(self.auto_logout)
        self.session_display_timer = QTimer(self)
        self.session_display_timer.timeout.connect(self.update_session_display)

        self.session_label = QLabel("Осталось: 10:00")
        self.session_label.setStyleSheet("font-size: 16px; color: white;")
        layout.addWidget(self.session_label)
        self.reset_session_timer()
        self.installEventFilter(self)

        filter_layout = QHBoxLayout()
        self.role_filter = QComboBox()
        self.role_filter.addItems(["Все роли", "admin", "researcher", "lab_assistant", "accountant"])
        filter_layout.addWidget(self.role_filter)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по логину или ФИО")
        filter_layout.addWidget(self.search_input)

        layout.addLayout(filter_layout)

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(["ID", "Логин", "ФИО", "Роль", "Последний вход"])
        self.user_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.user_table.customContextMenuRequested.connect(self.open_context_menu)
        layout.addWidget(self.user_table)

        self.add_user_button = QPushButton("Добавить пользователя")
        layout.addWidget(self.add_user_button)

        self.refresh_button = QPushButton("Обновить список пользователей")
        layout.addWidget(self.refresh_button)

        self.toggle_archive_button = QPushButton("Показать архив пользователей")
        layout.addWidget(self.toggle_archive_button)

        self.logout_button = QPushButton("Выход из панели администратора")
        layout.addWidget(self.logout_button)

        self.add_user_button.clicked.connect(self.add_user)
        self.refresh_button.clicked.connect(self.refresh_users)
        self.toggle_archive_button.clicked.connect(self.toggle_archive_view)
        self.logout_button.clicked.connect(self.logout)
        self.user_table.cellDoubleClicked.connect(self.edit_user)
        self.role_filter.currentIndexChanged.connect(self.refresh_users)
        self.search_input.textChanged.connect(self.refresh_users)

        central_widget.setLayout(layout)

        self.refresh_users()

        self.order_button = QPushButton("Приём биоматериала")
        layout.addWidget(self.order_button)
        self.order_button.clicked.connect(self.open_order_panel)

        self.patient_button = QPushButton("Пациенты")
        layout.addWidget(self.patient_button)
        self.patient_button.clicked.connect(self.open_patient_panel)
        self.login_history_button = QPushButton("История входов")
        layout.addWidget(self.login_history_button)
        self.login_history_button.clicked.connect(self.open_login_history)


    def open_patient_panel(self):
        self.patient_panel = PatientPanel()
        self.patient_panel.show()

    def refresh_users(self):
        try:
            users = self.db.get_users(archived=self.showing_archive)

            role = self.role_filter.currentText()
            search_text = self.search_input.text().strip().lower()

            if role != "Все роли":
                users = [user for user in users if user['role'] == role]

            if search_text:
                users = [user for user in users if search_text in user['login'].lower() or search_text in user['full_name'].lower()]

            self.user_table.setRowCount(len(users))
            for row_idx, user in enumerate(users):
                self.user_table.setItem(row_idx, 0, QTableWidgetItem(str(user['id'])))
                self.user_table.setItem(row_idx, 1, QTableWidgetItem(user['login']))
                self.user_table.setItem(row_idx, 2, QTableWidgetItem(user['full_name']))
                self.user_table.setItem(row_idx, 3, QTableWidgetItem(user['role']))
                last_login = user['last_login'].strftime("%Y-%m-%d %H:%M:%S") if user['last_login'] else "Нет данных"
                self.user_table.setItem(row_idx, 4, QTableWidgetItem(last_login))
        except Exception as e:
            print(f"Ошибка обновления пользователей: {e}")

    def add_user(self):
        self.add_user_dialog = AddUserDialog()
        if self.add_user_dialog.exec():
            self.refresh_users()

    def edit_user(self, row, column):
        user_id = int(self.user_table.item(row, 0).text())
        login = self.user_table.item(row, 1).text()
        full_name = self.user_table.item(row, 2).text()
        role = self.user_table.item(row, 3).text()

        self.edit_dialog = EditUserDialog(user_id, login, full_name, role)
        if self.edit_dialog.exec():
            self.refresh_users()

    def open_context_menu(self, position):
        menu = QMenu()

        if self.showing_archive:
            restore_action = menu.addAction("Восстановить пользователя")
        else:
            archive_action = menu.addAction("Архивировать пользователя")

        action = menu.exec(self.user_table.viewport().mapToGlobal(position))

        selected_row = self.user_table.currentRow()
        if selected_row == -1:
            return

        user_id = int(self.user_table.item(selected_row, 0).text())

        if not self.showing_archive and action == archive_action:
            confirm = QMessageBox.question(self, "Архивирование пользователя", "Вы уверены, что хотите архивировать этого пользователя?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    self.db.archive_user(user_id)
                    QMessageBox.information(self, "Успех", "Пользователь архивирован успешно!")
                    self.refresh_users()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось архивировать пользователя: {e}")

        if self.showing_archive and action == restore_action:
            confirm = QMessageBox.question(self, "Восстановление пользователя", "Вы уверены, что хотите восстановить этого пользователя?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    self.db.restore_user(user_id)
                    QMessageBox.information(self, "Успех", "Пользователь восстановлен успешно!")
                    self.refresh_users()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось восстановить пользователя: {e}")

    def toggle_archive_view(self):
        self.showing_archive = not self.showing_archive
        self.toggle_archive_button.setText(
            "Показать активных пользователей" if self.showing_archive else "Показать архив пользователей"
        )
        self.refresh_users()

    def logout(self):
        from auth.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def open_order_panel(self):
        self.order_panel = OrderPanel()
        self.order_panel.show()

    def open_login_history(self):
        from ui.login_history import LoginHistoryDialog
        self.login_history_dialog = LoginHistoryDialog()
        self.login_history_dialog.show()

    def reset_session_timer(self):
        self.session_time_left = 600

        # Обновление отображения времени
        self.session_display_timer.stop()
        self.session_display_timer.timeout.disconnect()
        self.session_display_timer.timeout.connect(self.update_session_display)
        self.session_display_timer.start(1000)

        # ⬅️ Добавляем запуск таймера выхода
        self.session_timer.stop()
        self.session_timer.timeout.disconnect()
        self.session_timer.timeout.connect(self.auto_logout)
        self.session_timer.start(600_000)  # 10 минут = 600000 мс

    def update_session_display(self):
        self.session_time_left -= 1
        minutes = self.session_time_left // 60
        seconds = self.session_time_left % 60
        self.session_label.setText(f"Осталось: {minutes:02}:{seconds:02}")
        if self.session_time_left <= 0:
            self.session_display_timer.stop()
            # Автоматический выход произойдёт через session_timer

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Type.MouseMove, QEvent.Type.KeyPress):
            self.reset_session_timer()
        return super().eventFilter(obj, event)

    def auto_logout(self):
        print("[DEBUG] auto_logout вызван")
        QMessageBox.information(self, "Сеанс", "Время сессии истекло. Возврат к окну входа.")
        from auth.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()  # <-- безопасно закрываем старое окно

    '''def safe_restart(self):
        print("[LOG] soft restart admin panel")
        self.new_window = AdminPanel()
        self.new_window.show()
        QTimer.singleShot(100, self.close)  # ⬅️ чуть безопаснее, чем сразу close()'''


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = AdminPanel()
    window.show()
    sys.exit(app.exec())
