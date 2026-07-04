import json
import os
from datetime import datetime


class HistoryStore:

    def __init__(self, logger, file_path="analysis/storage/history.jsonl"):
        self.logger = logger
        self.file_path = file_path

        # ساخت مسیر اگر وجود ندارد
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    # ======================================================
    # SAVE REPORT
    # ======================================================
    def save(self, report):

        record = {
            "timestamp": datetime.now().isoformat(),
            "data": report
        }

        try:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

        except Exception as e:
            self.logger.error(f"History save error: {str(e)}")

    # ======================================================
    # LOAD HISTORY
    # ======================================================
    def load_all(self):

        if not os.path.exists(self.file_path):
            return []

        data = []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    data.append(json.loads(line.strip()))

        except Exception as e:
            self.logger.error(f"History load error: {str(e)}")

        return data

    # ======================================================
    # GET LAST N RECORDS
    # ======================================================
    def last_n(self, n=10):

        all_data = self.load_all()

        return all_data[-n:]
