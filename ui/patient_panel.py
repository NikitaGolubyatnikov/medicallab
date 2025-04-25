# 📂 Файл: ui/patient_panel.py

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QDialog, QMenu
)
from bd.database import Database
from PyQt6.QtCore import Qt, QPoint
from datetime import datetime

class PatientPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пациенты")
        self.setFixedSize(1000, 700)

        self.db = Database()
        self.showing_archive = False

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Список пациентов")
        title.setStyleSheet("font-size: 18px; font-weight: bold")
        layout.addWidget(title)

        top_bar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по ФИО или телефону")
        self.search_input.textChanged.connect(self.refresh_table)

        self.filter_box = QComboBox()
        self.filter_box.addItems(["Все", "С полисом", "Без полиса", "Есть email", "Нет email"])
        self.filter_box.currentIndexChanged.connect(self.refresh_table)

        self.toggle_archive_btn = QPushButton("Показать архив")
        self.toggle_archive_btn.clicked.connect(self.toggle_archive_view)

        top_bar.addWidget(self.search_input)
        top_bar.addWidget(self.filter_box)
        top_bar.addWidget(self.toggle_archive_btn)
        layout.addLayout(top_bar)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "ФИО", "Дата рождения", "Телефон", "Email", "Страховка"
        ])
        self.table.cellDoubleClicked.connect(self.edit_patient)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.table)

        self.add_btn = QPushButton("Добавить пациента")
        self.add_btn.clicked.connect(self.add_patient)
        layout.addWidget(self.add_btn)

        self.setLayout(layout)

        self.table.setSortingEnabled(True)

    def refresh_table(self):
        search_text = self.search_input.text().lower()
        filter_value = self.filter_box.currentText()
        patients = self.db.get_patients(archived=self.showing_archive)

        filtered = []
        for p in patients:
            if search_text and search_text not in p['full_name'].lower() and search_text not in (p['phone'] or '').lower():
                continue
            if filter_value == "С полисом" and not p['insurance_number']:
                continue
            if filter_value == "Без полиса" and p['insurance_number']:
                continue
            if filter_value == "Есть email" and not p['email']:
                continue
            if filter_value == "Нет email" and p['email']:
                continue
            filtered.append(p)

        self.table.setRowCount(len(filtered))
        for i, p in enumerate(filtered):
            self.table.setItem(i, 0, QTableWidgetItem(str(p['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(p['full_name']))
            self.table.setItem(i, 2, QTableWidgetItem(p['date_of_birth'].strftime("%Y-%m-%d") if p['date_of_birth'] else ""))
            self.table.setItem(i, 3, QTableWidgetItem(p['phone'] or ""))
            self.table.setItem(i, 4, QTableWidgetItem(p['email'] or ""))
            self.table.setItem(i, 5, QTableWidgetItem(p['insurance_type'] or ""))

    def toggle_archive_view(self):
        self.showing_archive = not self.showing_archive
        self.toggle_archive_btn.setText("Показать активных" if self.showing_archive else "Показать архив")
        self.refresh_table()

    def add_patient(self):
        dialog = PatientDialog()
        if dialog.exec():
            self.refresh_table()

    def edit_patient(self, row, _):
        patient_id = int(self.table.item(row, 0).text())
        dialog = PatientDialog(patient_id)
        if dialog.exec():
            self.refresh_table()

    def show_context_menu(self, pos: QPoint):
        index = self.table.indexAt(pos)
        if not index.isValid():
            return

        row = index.row()
        patient_id = int(self.table.item(row, 0).text())

        menu = QMenu()
        archive_action = menu.addAction("Архивировать" if not self.showing_archive else "Восстановить")
        action = menu.exec(self.table.mapToGlobal(pos))

        if action == archive_action:
            try:
                self.db.set_patient_archive(patient_id, archive=not self.showing_archive)
                QMessageBox.information(self, "Готово", "Статус пациента обновлён")
                self.refresh_table()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

class PatientDialog(QDialog):
    def __init__(self, patient_id=None):
        super().__init__()
        self.db = Database()
        self.patient_id = patient_id

        self.setWindowTitle("Редактирование пациента" if patient_id else "Добавление пациента")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()
        self.inputs = {}

        for label in ["ФИО", "Дата рождения (YYYY-MM-DD)", "Телефон", "Email", "Паспорт", "Номер страховки", "Тип страховки"]:
            layout.addWidget(QLabel(label))
            inp = QLineEdit()
            self.inputs[label] = inp
            layout.addWidget(inp)

        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        if patient_id:
            self.load_patient()

    def load_patient(self):
        p = self.db.get_patient_by_id(self.patient_id)
        if p:
            self.inputs["ФИО"].setText(p['full_name'])
            self.inputs["Дата рождения (YYYY-MM-DD)"].setText(str(p['date_of_birth']) if p['date_of_birth'] else "")
            self.inputs["Телефон"].setText(p['phone'] or "")
            self.inputs["Email"].setText(p['email'] or "")
            self.inputs["Паспорт"].setText(p['passport_series_number'] or "")
            self.inputs["Номер страховки"].setText(p['insurance_number'] or "")
            self.inputs["Тип страховки"].setText(p['insurance_type'] or "")

    def save(self):
        date_str = self.inputs["Дата рождения (YYYY-MM-DD)"].text().strip()
        try:
            date_of_birth = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Дата рождения должна быть в формате ГГГГ-ММ-ДД (например: 1990-12-31)")
            return

        data = {
            'full_name': self.inputs["ФИО"].text().strip(),
            'date_of_birth': date_of_birth,
            'phone': self.inputs["Телефон"].text().strip(),
            'email': self.inputs["Email"].text().strip(),
            'passport_series_number': self.inputs["Паспорт"].text().strip(),
            'insurance_number': self.inputs["Номер страховки"].text().strip(),
            'insurance_type': self.inputs["Тип страховки"].text().strip()
        }

        try:
            if self.patient_id:
                self.db.update_patient(self.patient_id, data)
            else:
                self.db.add_patient(
                    data['full_name'],
                    data['date_of_birth'],
                    data['passport_series_number'],
                    data['phone'],
                    data['email'],
                    data['insurance_number'],
                    data['insurance_type']
                )

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить: {e}")

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = PatientPanel()
    win.show()
    sys.exit(app.exec())
