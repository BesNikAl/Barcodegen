from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PIL import Image
from PIL.ImageQt import ImageQt  # Для конвертации PIL -> QImage/QPixmap
from io import BytesIO
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

    def set_pixmap(self, pil_image: Image.Image | None):

        if pil_image is None:
            self.original_pixmap = None
            self.preview_label.clear()
            return

        # Безопасная конвертация PIL -> QPixmap (избегаем ImageQt.toqpixmap крашей)
        buffer = BytesIO()
        pil_image.save(buffer, format="PNG")
        buffer.seek(0)

        qt_image = QImage.fromData(buffer.getvalue())
        self.original_pixmap = QPixmap.fromImage(qt_image)

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