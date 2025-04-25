# core/session.py

import time

class SessionManager:
    def __init__(self):
        self.blocked_until = 0

    def is_blocked(self) -> bool:
        """Проверяет, заблокирован ли пользователь"""
        return time.time() < self.blocked_until

    def block(self):
        """Блокирует пользователя на определённое время"""
        self.blocked_until = time.time() + 60  # Блокировка на 60 секунд

    def unblock(self):
        """Снимает блокировку"""
        self.blocked_until = 0

    def get_block_time_left(self) -> int:
        """Сколько осталось секунд блокировки"""
        remaining = self.blocked_until - time.time()
        return int(remaining) if remaining > 0 else 0
