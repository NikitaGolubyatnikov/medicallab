from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QLabel
from bd.database import Database

class LoginHistoryDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("История входов в систему")
        self.resize(800, 500)
        self.db = Database()

        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Фильтр по логину...")
        self.search_input.textChanged.connect(self.refresh)
        layout.addWidget(QLabel("Фильтр:"))
        layout.addWidget(self.search_input)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Логин", "Дата/время", "Успешно?"])
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.refresh()

    def refresh(self):
        rows = self.db.get_login_logs(self.search_input.text().strip())
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(row['login']))
            self.table.setItem(i, 1, QTableWidgetItem(str(row['attempt_time'])))
            self.table.setItem(i, 2, QTableWidgetItem("✅" if row['success'] else "❌"))
