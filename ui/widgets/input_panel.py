from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QTextEdit,      # ← изменили
    QPushButton,
    QHBoxLayout
)
from PyQt6.QtCore import Qt


class InputPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        self.lbl_data = QLabel("Данные:")

        self.txt_data = QTextEdit()
        self.txt_data.setMaximumHeight(60)  # ← Ограничиваем высоту
        self.txt_data.setMinimumHeight(35)  # минимальная высота
        self.txt_data.setPlaceholderText(
            "Введите данные для DataMatrix... (GS поддерживается)"
        )

        self.btn_add = QPushButton("Добавить")

        layout.addWidget(self.lbl_data)
        layout.addWidget(self.txt_data)
        layout.addWidget(self.btn_add)