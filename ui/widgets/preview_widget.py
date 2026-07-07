from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QScrollArea
)


class PreviewWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scale_percent = 100
        self.original_pixmap = None

        layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.scroll_area.setWidget(
            self.preview_label
        )

        layout.addWidget(self.scroll_area)

    def set_pixmap(self, pixmap: QPixmap):

        self.original_pixmap = pixmap

        self.update_scale()

    def set_scale(self, percent: int):

        self.scale_percent = percent

        self.update_scale()

    def update_scale(self):

        if self.original_pixmap is None:
            return

        width = int(
            self.original_pixmap.width()
            * self.scale_percent
            / 100
        )

        height = int(
            self.original_pixmap.height()
            * self.scale_percent
            / 100
        )

        scaled = self.original_pixmap.scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

        self.preview_label.setPixmap(
            scaled
        )