# 📂 Файл: ui/accountant_panel.py
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, QEvent
from core.financial_report import FinancialReportWindow
import os

class AccountantPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель Бухгалтера")
        self.setGeometry(100, 100, 500, 300)

        layout = QVBoxLayout()

        self.session_time_left = 600
        self.session_timer = QTimer(self)
        self.session_timer.timeout.connect(self.auto_logout)
        self.session_display_timer = QTimer(self)
        self.session_display_timer.timeout.connect(self.update_session_display)

        self.session_label = QLabel("Осталось: 10:00")
        self.session_label.setStyleSheet("font-size: 14px; color: white;")

        self.reset_session_timer()
        self.installEventFilter(self)

        # Фото бухгалтера
        DIR = os.path.dirname(os.path.abspath(__file__))
        avatar_path = os.path.normpath(os.path.join(DIR, "..", "resources", "bukhgalter.jpeg"))
        self.avatar = QLabel()
        self.avatar.setFixedSize(164, 164)
        pix = QPixmap(avatar_path)
        if not pix.isNull():
            self.avatar.setPixmap(pix.scaled(164, 164, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.avatar.setText("⚠ Нет аватарки")
        layout.addWidget(self.avatar)

        self.title = QLabel("Вы вошли как Бухгалтер")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.title)
        layout.addWidget(self.session_label)

        self.report_btn = QPushButton("📄 Финансовый отчёт")
        self.report_btn.clicked.connect(self.show_report)
        layout.addWidget(self.report_btn)

        self.logout_btn = QPushButton("Выйти")
        self.logout_btn.clicked.connect(self.logout)
        layout.addWidget(self.logout_btn)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

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

    def show_report(self):
        self.rw = FinancialReportWindow()
        self.rw.exec()

    def logout(self):
        from auth.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = AccountantPanel()
    win.show()
    sys.exit(app.exec())
