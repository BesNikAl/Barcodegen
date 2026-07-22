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
        layout.setContentsMargins(0, 0, 0, 0)  # убираем отступы

        self.lbl_data = QLabel("Данные:")

        # QTextEdit с высотой как у кнопки
        self.txt_data = QTextEdit()
        self.txt_data.setMaximumHeight(36)
        self.txt_data.setMinimumHeight(36)
        self.txt_data.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # убираем скролл
        self.txt_data.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # центрирование по вертикали
        self.txt_data.setPlaceholderText(
            "Введите данные для DataMatrix... (GS поддерживается)"
        )

        self.btn_add = QPushButton("Добавить")

        layout.addWidget(self.lbl_data)
        layout.addWidget(self.txt_data)
        layout.addWidget(self.btn_add)