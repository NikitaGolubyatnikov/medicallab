# 📂 core/financial_report.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QFileDialog, QMessageBox
)
from bd.database import Database
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import openpyxl

class FinancialReportWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Финансовый отчёт - MedicalLab")
        self.setFixedSize(800, 500)

        self.db = Database()
        layout = QVBoxLayout()

        self.title = QLabel("💰 Финансовый отчёт по заказам")
        layout.addWidget(self.title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID заказа", "Код пробирки", "Сумма (₽)"])
        self.table.setSortingEnabled(True)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 120)
        layout.addWidget(self.table)

        self.total_label = QLabel("Общая сумма: ₽0.00")
        layout.addWidget(self.total_label)

        self.export_btn = QPushButton("Экспорт в PDF")
        layout.addWidget(self.export_btn)
        self.export_btn.clicked.connect(self.export_pdf)

        self.export_excel_btn = QPushButton("Экспорт в Excel")
        layout.addWidget(self.export_excel_btn)
        self.export_excel_btn.clicked.connect(self.export_excel)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        try:
            orders = self.db.get_all_orders()
            total = 0.0
            self.table.setRowCount(len(orders))

            for i, order in enumerate(orders):
                services = self.db.get_order_services(order['id'])
                cost = sum(float(s['cost']) for s in services)
                total += cost

                self.table.setItem(i, 0, QTableWidgetItem(str(order['id'])))
                self.table.setItem(i, 1, QTableWidgetItem(order['tube_code']))
                self.table.setItem(i, 2, QTableWidgetItem(f"{cost:.2f}"))

            self.total_label.setText(f"Общая сумма: ₽{total:,.2f}")
        except Exception as e:
            print("❌ Ошибка при загрузке отчёта:", e)

    def export_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить PDF", "financial_report.pdf", "PDF Files (*.pdf)")
        if not file_path:
            return

        try:
            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(width / 2, height - 2 * cm, "Финансовый отчёт - MedicalLab")

            y = height - 3 * cm
            c.setFont("Helvetica-Bold", 10)
            c.drawString(2 * cm, y, "ID заказа")
            c.drawString(6 * cm, y, "Код пробирки")
            c.drawString(12 * cm, y, "Сумма (₽)")

            y -= 0.7 * cm
            c.setFont("Helvetica", 10)
            for row in range(self.table.rowCount()):
                if y < 2 * cm:
                    c.showPage()
                    y = height - 2 * cm
                id_val = self.table.item(row, 0).text()
                tube = self.table.item(row, 1).text()
                cost = self.table.item(row, 2).text()
                c.drawString(2 * cm, y, id_val)
                c.drawString(6 * cm, y, tube)
                c.drawString(12 * cm, y, cost)
                y -= 0.6 * cm

            y -= cm
            c.setFont("Helvetica-Bold", 12)
            c.drawString(2 * cm, y, self.total_label.text())

            c.save()
            QMessageBox.information(self, "Успех", f"PDF сохранён: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте PDF:\n{e}")

    def export_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить Excel", "financial_report.xlsx", "Excel Files (*.xlsx)")
        if not file_path:
            return

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Финансовый отчёт"
            ws.append(["ID заказа", "Код пробирки", "Сумма (₽)"])

            for row in range(self.table.rowCount()):
                id_val = self.table.item(row, 0).text()
                tube = self.table.item(row, 1).text()
                cost = self.table.item(row, 2).text()
                ws.append([id_val, tube, cost])

            ws.append([])
            ws.append(["ИТОГО", "", self.total_label.text().split(':')[-1].strip()])

            wb.save(file_path)
            QMessageBox.information(self, "Успех", f"Excel сохранён: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте Excel:\n{e}")
