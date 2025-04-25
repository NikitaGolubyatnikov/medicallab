# 📂 Файл: ui/research_assistant_panel.py
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox,
    QComboBox, QTableWidget, QTableWidgetItem, QProgressBar, QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer, QEvent
from PyQt6.QtGui import QPixmap, QMovie
from core.research_report import ResearchReportWindow
from core.analyzer_api import AnalyzerAPI
from bd.database import Database
from ui.quality_report import QualityReportWindow
import openpyxl
import os

class ResearchAssistantPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель Научного Сотрудника")
        self.setGeometry(100, 100, 1000, 600)

        self.db = Database()

        self.analyzer_box = QComboBox()
        self.analyzer_box.addItems(["Ledetect", "Biorad"])

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["ID заказа", "Пациент", "Услуга", "Статус", "Результат"])

        self.progress = QProgressBar()

        # Таймер сессии и отображение
        self.session_time_left = 600
        self.session_timer = QTimer(self)
        self.session_timer.timeout.connect(self.auto_logout)
        self.session_display_timer = QTimer(self)
        self.session_display_timer.timeout.connect(self.update_session_display)

        self.session_label = QLabel("Осталось: 10:00")
        self.session_label.setStyleSheet("font-size: 16px; color: white;")

        self.reset_session_timer()
        self.installEventFilter(self)

        # Фото сотрудника с абсолютным путём
        DIR = os.path.dirname(os.path.abspath(__file__))
        avatar_path = os.path.normpath(os.path.join(DIR, "..", "resources", "laborant_1.jpeg"))
        self.avatar = QLabel()
        self.avatar.setFixedSize(64, 64)
        pix = QPixmap(avatar_path)
        if not pix.isNull():
            self.avatar.setPixmap(pix.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.avatar.setText("⚠ Нет аватарки")

        # Анимация загрузки (loader.gif)
        loader_path = os.path.normpath(os.path.join(DIR, "..", "resources", "loader (1).gif"))
        self.loader = QLabel()
        self.loader.setFixedSize(78, 78)
        self.movie = QMovie(loader_path)
        self.loader.setMovie(self.movie)
        self.loader.setVisible(False)

        self.send_button = QPushButton("Отправить на исследование")
        self.send_button.clicked.connect(self.send_for_research)

        self.check_button = QPushButton("Проверить статус")
        self.check_button.clicked.connect(self.check_status)

        self.export_excel_btn = QPushButton("Экспорт в Excel")
        self.export_excel_btn.clicked.connect(self.export_excel)

        self.quality_btn = QPushButton("Контроль качества")
        self.quality_btn.clicked.connect(self.show_quality_report)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Вы вошли как Научный Сотрудник"))
        layout.addWidget(self.avatar)
        layout.addWidget(self.session_label)
        layout.addWidget(QLabel("Выбор анализатора:"))
        layout.addWidget(self.analyzer_box)
        layout.addWidget(self.order_table)
        layout.addWidget(self.progress)
        layout.addWidget(self.loader)

        btns = QHBoxLayout()
        btns.addWidget(self.send_button)
        btns.addWidget(self.check_button)
        btns.addWidget(self.export_excel_btn)
        btns.addWidget(self.quality_btn)
        layout.addLayout(btns)

        self.logout_button = QPushButton("Выйти")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

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

    def logout(self):
        from auth.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def load_orders(self):
        orders = self.db.get_all_orders()
        self.order_table.setRowCount(len(orders))
        for i, order in enumerate(orders):
            patient = self.db.get_patient_by_id(order['patient_id'])
            name = patient['full_name'] if patient else "—"
            self.order_table.setItem(i, 0, QTableWidgetItem(str(order['id'])))
            self.order_table.setItem(i, 1, QTableWidgetItem(name))
            self.order_table.setItem(i, 2, QTableWidgetItem("—"))
            self.order_table.setItem(i, 3, QTableWidgetItem("Ожидает"))
            self.order_table.setItem(i, 4, QTableWidgetItem("—"))

    def get_selected_order(self):
        row = self.order_table.currentRow()
        if row < 0:
            return None, None
        order_id = int(self.order_table.item(row, 0).text())
        return row, order_id

    def send_for_research(self):
        analyzer = self.analyzer_box.currentText()
        row, order_id = self.get_selected_order()
        if order_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ")
            return

        order = self.db.get_order_by_id(order_id)
        services = self.db.get_order_services(order_id)
        codes = [s.get('code') for s in services if 'code' in s or s.get('code')]

        def callback(status, data):
            QTimer.singleShot(0, lambda: self.handle_response(status, data, row))

        self.movie.start()
        self.loader.setVisible(True)
        AnalyzerAPI.send_to_analyzer(analyzer, order['patient_id'], codes, callback)

    def check_status(self):
        analyzer = self.analyzer_box.currentText()
        QTimer.singleShot(0, lambda: AnalyzerAPI.poll_analyzer(analyzer, self.delayed_poll))

    def delayed_poll(self, status, data):
        QTimer.singleShot(0, lambda: self.handle_poll(status, data))

    def handle_response(self, status, data, row):
        self.movie.stop()
        self.loader.setVisible(False)
        if status == 200:
            QMessageBox.information(self, "Успех", "Отправлено на исследование")
            self.order_table.setItem(row, 3, QTableWidgetItem("Отправлено"))
        else:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {data}")

    def handle_poll(self, status, data):
        if status == 200:
            if 'progress' in data:
                self.progress.setValue(data['progress'])
            elif 'services' in data:
                result_text = "; ".join(f"{s['serviceCode']}: {s['value']}" for s in data['services'])
                current_row = self.order_table.currentRow()
                if current_row >= 0:
                    self.order_table.setItem(current_row, 4, QTableWidgetItem(result_text))
                QMessageBox.information(self, "Результаты", result_text)
        else:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {data}")

    def export_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить Excel", "analyzer_results.xlsx", "Excel Files (*.xlsx)")
        if not file_path:
            return

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Результаты анализатора"
            ws.append(["ID заказа", "Пациент", "Услуга", "Статус", "Результат"])

            for row in range(self.order_table.rowCount()):
                row_data = [self.order_table.item(row, col).text() if self.order_table.item(row, col) else ""
                            for col in range(self.order_table.columnCount())]
                ws.append(row_data)

            wb.save(file_path)
            QMessageBox.information(self, "Успех", f"Excel сохранён: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте Excel:\n{e}")

    def show_quality_report(self):
        self.qw = QualityReportWindow()
        self.qw.show()

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = ResearchAssistantPanel()
    win.show()
    sys.exit(app.exec())
