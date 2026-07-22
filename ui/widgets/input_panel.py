from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout
)


class InputPanel(QWidget):

    def __init__(self):

        super().__init__()

        layout = QHBoxLayout(self)

        self.lbl_data = QLabel("Данные:")

        self.txt_data = QLineEdit()

        self.txt_data.setPlaceholderText(
            "Введите данные для DataMatrix..."
        )

        self.btn_add = QPushButton("Добавить")

        layout.addWidget(self.lbl_data)
        layout.addWidget(self.txt_data)
        layout.addWidget(self.btn_add)