import json
from pathlib import Path
from datetime import datetime

class HistoryManager:

    def __init__(self):

        self.file_name = Path("data/history.json")
        self.records = []

        self.load()

    def load(self):

        if not self.file_name.exists():
            return

        try:

            with open(self.file_name, "r", encoding="utf-8") as file:

                self.records = json.load(file)

        except Exception:

            self.records = []

    def save(self):

        self.file_name.parent.mkdir(exist_ok=True)

        with open(self.file_name, "w", encoding="utf-8") as file:

            json.dump(
                self.records,
                file,
                indent=4,
                ensure_ascii=False
            )

    def add(self, text: str, comment: str = ""):

        text = text.strip()

        if text == "":
            return False

        for record in self.records:

            if record["data"] == text:
                return False

        self.records.append({

            "data": text,
            "comment": comment,

            "datetime": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        })

        self.save()

        return True

    def remove(self, index):

        if 0 <= index < len(self.records):

            self.records.pop(index)

            self.save()

    def clear(self):

        self.records.clear()

        self.save()

    def get_all(self):

        return self.records

    def update(self, index: int, text: str) -> bool:

        text = text.strip()

        if text == "":
            return False

        for i, record in enumerate(self.records):

            if i != index and record["data"] == text:
                return False

        if 0 <= index < len(self.records):
            self.records[index]["data"] = text

            self.save()

            return True

        return False

    def update_comment(self, index: int, comment: str):

        if 0 <= index < len(self.records):
            self.records[index]["comment"] = comment

            self.save()

            return True

        return False