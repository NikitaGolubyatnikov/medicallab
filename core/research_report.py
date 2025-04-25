# 📂 core/research_report.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from bd.database import Database

class ResearchReportWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Научный отчёт - MedicalLab")
        self.setFixedSize(700, 500)

        self.db = Database()
        layout = QVBoxLayout()

        self.stats_label = QLabel("Анализ заказов:")
        layout.addWidget(self.stats_label)

        self.table = QTableWidget()
        self.table.setSortingEnabled(True) #сортировка
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        orders = self.db.get_all_orders()
        self.table.setRowCount(len(orders))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Пациент", "Пробирка", "Дата"])

        for i, order in enumerate(orders):
            self.table.setItem(i, 0, QTableWidgetItem(str(order['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(str(order['patient_id'])))
            self.table.setItem(i, 2, QTableWidgetItem(order['tube_code']))
            self.table.setItem(i, 3, QTableWidgetItem(str(order['created_at'])))

