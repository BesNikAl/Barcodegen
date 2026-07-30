from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSlider,
    QGroupBox,
)


class ZoomPanel(QWidget):
    """Панель масштаба. Отвечает только за отображение слайдера и метки."""

    zoom_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.group = QGroupBox("Масштаб")
        group_layout = QVBoxLayout()

        self.lbl_zoom = QLabel("100 %")
        self.lbl_zoom.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider_zoom = QSlider(Qt.Orientation.Vertical)
        self.slider_zoom.setMinimum(50)
        self.slider_zoom.setMaximum(500)
        self.slider_zoom.setValue(100)

        group_layout.addWidget(self.lbl_zoom)
        group_layout.addWidget(self.slider_zoom)
        self.group.setLayout(group_layout)

        layout.addWidget(self.group)

    def _connect_signals(self):
        self.slider_zoom.valueChanged.connect(self._on_slider_changed)

    def _on_slider_changed(self, value: int):
        self.lbl_zoom.setText(f"{value} %")
        self.zoom_changed.emit(value)

    def set_value(self, value: int):
        self.slider_zoom.setValue(value)

    def value(self) -> int:
        return self.slider_zoom.value()