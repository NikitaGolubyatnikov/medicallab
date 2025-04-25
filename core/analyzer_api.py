# 📂 Файл: core/analyzer_api.py
import threading
import time
import random

class AnalyzerAPI:
    progress_store = {}

    @staticmethod
    def send_to_analyzer(name: str, patient_id: int, service_codes: list[str], callback):
        def task():
            # Симуляция отправки с инициализацией прогресса
            AnalyzerAPI.progress_store[name] = 0
            time.sleep(1.5)
            callback(200, {"status": "started", "patient_id": patient_id, "services": service_codes})

        threading.Thread(target=task).start()

    @staticmethod
    def poll_analyzer(name: str, callback):
        def task():
            time.sleep(1)
            if name in AnalyzerAPI.progress_store:
                # Эмуляция нарастания прогресса
                progress = AnalyzerAPI.progress_store[name] + random.randint(10, 25)
                if progress >= 100:
                    del AnalyzerAPI.progress_store[name]
                    callback(200, {
                        "services": [
                            {"serviceCode": "HGB", "value": "13.4 г/дл"},
                            {"serviceCode": "WBC", "value": "6.1 x10^9/л"}
                        ]
                    })
                else:
                    AnalyzerAPI.progress_store[name] = progress
                    callback(200, {"progress": min(progress, 100)})
            else:
                callback(404, "Анализатор не запущен")

        threading.Thread(target=task).start()
