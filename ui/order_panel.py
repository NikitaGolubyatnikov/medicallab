# 📂 Файл: ui/order_panel.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QLineEdit, QComboBox, QListWidget, QListWidgetItem, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QCheckBox
)
from bd.database import Database
from PyQt6.QtCore import Qt
from core.barcode_generator import generate_pdf_report_for_order
import os

class OrderPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приём биоматериала")
        self.setMinimumSize(700, 500)

        self.db = Database()
        self.selected_services = []
        self.total_cost = 0.0
        self.showing_archive = False

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Формирование заказа"))

        self.patient_box = QComboBox()
        self.patient_map = {}
        for patient in self.db.get_patients():
            pid = patient['id']
            name = patient['full_name']
            label = f"{name} ({pid})"
            self.patient_box.addItem(label)
            self.patient_map[label] = pid
        layout.addWidget(self.patient_box)

        self.tube_code_hidden = QLabel("Код пробирки будет сгенерирован автоматически")
        layout.addWidget(self.tube_code_hidden)

        service_layout = QHBoxLayout()
        self.service_selector = QComboBox()
        self.service_selector.setEditable(True)
        self.service_map = {}
        if hasattr(self.db, 'get_all_services'):
            for code, name, cost in self.db.get_all_services():
                label = f"{name} ({code}) — {float(cost):.2f} ₽"
                self.service_selector.addItem(label)
                self.service_map[label] = (code, cost)
        service_layout.addWidget(self.service_selector)

        self.add_service_btn = QPushButton("Добавить услугу")
        self.add_service_btn.clicked.connect(self.add_service)
        service_layout.addWidget(self.add_service_btn)

        layout.addLayout(service_layout)

        self.service_list = QListWidget()
        layout.addWidget(self.service_list)

        self.total_label = QLabel("Общая стоимость: 0.00 ₽")
        layout.addWidget(self.total_label)

        self.create_btn = QPushButton("Создать заказ")
        self.create_btn.clicked.connect(self.create_order)
        layout.addWidget(self.create_btn)

        self.toggle_archive = QCheckBox("Показать архив")
        self.toggle_archive.stateChanged.connect(self.toggle_archive_view)
        layout.addWidget(self.toggle_archive)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(["ID", "Пациент", "Пробирка", "Дата"])
        layout.addWidget(self.orders_table)

        self.archive_btn = QPushButton("Архивировать заказ")
        self.archive_btn.clicked.connect(self.archive_selected_order)
        layout.addWidget(self.archive_btn)

        self.setLayout(layout)
        self.load_orders()

    def add_service(self):
        label = self.service_selector.currentText()
        if label in self.service_map:
            code, cost = self.service_map[label]
            self.selected_services.append(code)
            self.total_cost += float(cost)
            self.service_list.addItem(f"{label}")
            self.total_label.setText(f"Общая стоимость: {self.total_cost:.2f} ₽")

    def create_order(self):
        try:
            patient_label = self.patient_box.currentText()
            patient_id = self.patient_map.get(patient_label)

            if not patient_id or not self.selected_services:
                raise ValueError("Укажите пациента и хотя бы одну услугу")

            order_id = self.db.create_order(patient_id, None, self.selected_services)
            patient_data = self.db.get_patient_by_id(patient_id)
            services = self.db.get_order_services(order_id)

            for s in services:
                s["name"] = "Анализ крови"
                s["code"] = s.get("service_id", "–")
                s["value"] = "—"

            pdf_path, _ = generate_pdf_report_for_order(order_id, patient_data, services)

            abs_path = os.path.abspath(pdf_path)
            QMessageBox.information(
                self,
                "Успех",
                f"Заказ #{order_id} создан!\nPDF заказа: {abs_path}"
            )
            self.clear()
            self.load_orders()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать заказ: {e}")

    def clear(self):
        self.service_list.clear()
        self.selected_services.clear()
        self.total_cost = 0.0
        self.total_label.setText("Общая стоимость: 0.00 ₽")

    def load_orders(self):
        orders = self.db.get_all_orders(archived=self.showing_archive)
        self.orders_table.setRowCount(len(orders))
        for i, order in enumerate(orders):
            patient = self.db.get_patient_by_id(order["patient_id"])
            name = patient["full_name"] if patient else "—"
            self.orders_table.setItem(i, 0, QTableWidgetItem(str(order["id"])))
            self.orders_table.setItem(i, 1, QTableWidgetItem(name))
            self.orders_table.setItem(i, 2, QTableWidgetItem(order["tube_code"]))
            self.orders_table.setItem(i, 3, QTableWidgetItem(str(order["created_at"])))

    def archive_selected_order(self):
        row = self.orders_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для архивирования")
            return

        order_id = int(self.orders_table.item(row, 0).text())
        self.db.archive_order(order_id)
        QMessageBox.information(self, "Готово", "Заказ архивирован")
        self.load_orders()

    def toggle_archive_view(self):
        self.showing_archive = self.toggle_archive.isChecked()
        self.load_orders()

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = OrderPanel()
    win.show()
    sys.exit(app.exec())