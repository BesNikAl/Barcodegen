from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QGroupBox,
)

from core.validator import Validator


class HistoryTable(QWidget):
    """Таблица истории. Отвечает только за отображение. Не работает с JSON."""

    current_row_changed = pyqtSignal(int)
    data_edited = pyqtSignal(int, str)      # row, display_text
    comment_edited = pyqtSignal(int, str)   # row, comment

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.group = QGroupBox("История")
        group_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["id", "Данные", "Комментарий"])

        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionsMovable(False)
        header.setCascadingSectionResizes(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        group_layout.addWidget(self.table)
        self.group.setLayout(group_layout)
        layout.addWidget(self.group)

    def _connect_signals(self):
        self.table.currentCellChanged.connect(self._on_current_changed)
        self.table.itemChanged.connect(self._on_item_changed)

    def _on_current_changed(
        self,
        current_row: int,
        current_column: int,
        previous_row: int,
        previous_column: int,
    ):
        if current_row >= 0:
            self.current_row_changed.emit(current_row)

    def _on_item_changed(self, item: QTableWidgetItem):
        row = item.row()
        if item.column() == 1:
            self.data_edited.emit(row, item.text())
        elif item.column() == 2:
            self.comment_edited.emit(row, item.text())

    def update_records(self, records: list):
        """Обновляет таблицу по списку записей из HistoryManager."""
        self.table.blockSignals(True)

        self.table.setRowCount(len(records))

        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))

            display_data = Validator.normalize_for_display(record["data"])
            self.table.setItem(row, 1, QTableWidgetItem(display_data))

            self.table.setItem(
                row, 2, QTableWidgetItem(record.get("comment", ""))
            )

        self.table.resizeColumnsToContents()

        free_space = (
            self.table.viewport().width()
            - self.table.columnWidth(0)
            - self.table.columnWidth(2)
        )
        if free_space > self.table.columnWidth(1):
            self.table.setColumnWidth(1, free_space)

        self.table.blockSignals(False)

    def current_row(self) -> int:
        return self.table.currentRow()