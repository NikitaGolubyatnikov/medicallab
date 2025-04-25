# 📂 Файл: ui/quality_report.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

class QualityReportWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("График контроля качества")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        self.label = QLabel("📊 Контроль качества анализов")
        layout.addWidget(self.label)

        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.plot_graph)
        layout.addWidget(self.plot_button)

        self.canvas = FigureCanvas(Figure())
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def plot_graph(self):
        x = list(range(1, 21))
        y = [round(random.uniform(10, 15), 2) for _ in x]

        ax = self.canvas.figure.subplots()
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(x, y, marker='o')
        ax.set_title("Уровень гемоглобина")
        ax.set_xlabel("Номер анализа")
        ax.set_ylabel("HGB (г/дл)")
        ax.grid(True)

        self.canvas.draw()