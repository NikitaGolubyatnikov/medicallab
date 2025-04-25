# 📂 Файл: ui/lab_assistant_panel.py
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit, QHBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, QEvent
from ui.order_panel import OrderPanel
from bd.database import Database
import os

class LabAssistantPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель Лаборанта")
        self.setGeometry(100, 100, 800, 600)

        self.db = Database()

        self.session_time_left = 600
        self.session_timer = QTimer(self)
        self.session_timer.timeout.connect(self.auto_logout)
        self.session_display_timer = QTimer(self)
        self.session_display_timer.timeout.connect(self.update_session_display)

        self.session_label = QLabel("Осталось: 10:00")
        self.session_label.setStyleSheet("font-size: 16px; color: white;")

        self.reset_session_timer()
        self.installEventFilter(self)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Фото лаборанта (абсолютный путь)
        DIR = os.path.dirname(os.path.abspath(__file__))
        avatar_path = os.path.normpath(os.path.join(DIR, "..", "resources", "laborant_2.png"))
        self.avatar = QLabel()
        self.avatar.setFixedSize(100, 100)
        pix = QPixmap(avatar_path)
        if not pix.isNull():
            self.avatar.setPixmap(pix.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.avatar.setText("⚠ Нет аватарки")
        layout.addWidget(self.avatar)

        self.title_label = QLabel("Вы вошли как Лаборант")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title_label)

        layout.addWidget(self.session_label)

        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Фильтр по имени пациента")
        self.filter_input.textChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.filter_input)
        layout.addLayout(filter_layout)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(["ID", "Пациент", "Пробирка", "Дата"])
        self.orders_table.setSortingEnabled(True)
        layout.addWidget(self.orders_table)

        self.order_button = QPushButton("Приём биоматериала")
        layout.addWidget(self.order_button)
        self.order_button.clicked.connect(self.open_orders)

        self.logout_button = QPushButton("Выйти")
        layout.addWidget(self.logout_button)
        self.logout_button.clicked.connect(self.logout)

        central_widget.setLayout(layout)
        self.load_orders()

    def reset_session_timer(self):
        self.session_time_left = 600
        self.session_timer.start(600000)
        self.session_display_timer.start(1000)
        self.update_session_display()

    def update_session_display(self):
        self.session_time_left -= 1
        minutes = self.session_time_left // 60
        seconds = self.session_time_left % 60
        self.session_label.setText(f"Осталось: {minutes:02}:{seconds:02}")
        if self.session_time_left <= 0:
            self.session_display_timer.stop()

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Type.MouseMove, QEvent.Type.KeyPress):
            self.reset_session_timer()
        return super().eventFilter(obj, event)

    def auto_logout(self):
        from core.session import SessionManager
        sm = SessionManager()
        sm.block()
        QMessageBox.information(self, "Сеанс завершён", "Вы были автоматически выведены из системы из-за бездействия.")
        self.logout()

    def open_orders(self):
        self.order_panel = OrderPanel()
        self.order_panel.show()

    def logout(self):
        from auth.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def load_orders(self):
        self.orders = self.db.get_all_orders()
        self.display_orders(self.orders)

    def display_orders(self, orders):
        self.orders_table.setRowCount(len(orders))
        for i, order in enumerate(orders):
            patient = self.db.get_patient_by_id(order["patient_id"])
            name = patient["full_name"] if patient else "—"
            self.orders_table.setItem(i, 0, QTableWidgetItem(str(order["id"])))
            self.orders_table.setItem(i, 1, QTableWidgetItem(name))
            self.orders_table.setItem(i, 2, QTableWidgetItem(order["tube_code"]))
            self.orders_table.setItem(i, 3, QTableWidgetItem(str(order["created_at"])))

    def apply_filter(self):
        query = self.filter_input.text().strip().lower()
        filtered = []
        for order in self.orders:
            patient = self.db.get_patient_by_id(order["patient_id"])
            name = patient["full_name"] if patient else ""
            if query in name.lower():
                filtered.append(order)
        self.display_orders(filtered)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = LabAssistantPanel()
    win.show()
    sys.exit(app.exec())
