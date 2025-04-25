# 📂 Файл: main.py
import sys
import logging
from PyQt6.QtWidgets import QApplication
from auth.login_window import LoginWindow

class LogFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',     # синий
        'INFO': '\033[92m',      # зелёный
        'WARNING': '\033[93m',   # жёлтый
        'ERROR': '\033[91m',     # красный
        'CRITICAL': '\033[95m'   # фиолетовый
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"

handler = logging.StreamHandler()
handler.setFormatter(LogFormatter("%(levelname)s:%(name)s:%(message)s"))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.handlers = [handler]

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()