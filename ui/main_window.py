from core.datamatrix_generator import DataMatrixGenerator
from core.history_manager import HistoryManager
from core.csv_importer import CsvImporter
from core.validator import Validator
from ui.widgets.input_panel import InputPanel
from core.settings import get_app_path
from pathlib import Path
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import re
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QGroupBox,
    QSplitter,
    QSlider,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QFileDialog
)


from ui.widgets.preview_widget import PreviewWidget
from ui.styles.dark_theme import get_dark_stylesheet


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("BarCodeGen")
        if getattr(sys, "frozen", False):
            base_path = Path(sys.executable).resolve().parent
        else:
            base_path = Path(__file__).resolve().parents[2]

        icon_path = get_app_path(
            "resources",
            "icons",
            "Barcodegen.ico",
        )

        self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(1000, 700)
        self.setMinimumSize(1000, 700)

        self.init_ui()
        self.apply_dark_theme()

        self.generator = DataMatrixGenerator()
        self.history = HistoryManager()

        self.connect_signals()

        # Заполнить таблицу из history.json
        self.update_history_table()

        self.statusBar().showMessage("Готово")

    def init_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        self.input_panel = InputPanel()

        main_layout.addWidget(
            self.input_panel
        )

        # ==================================================
        # Центральная область
        # ==================================================

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Левая панель (кнопки)

        buttons_group = QGroupBox("Управление")

        buttons_layout = QVBoxLayout()

        self.btn_delete = QPushButton("Удалить")
        self.btn_clear = QPushButton("Очистить")
        self.btn_import_csv = QPushButton("Импорт CSV")

        # Скругление для всех кнопок (включая "Добавить")
        button_style = """
                    QPushButton {
                        border-radius: 6px;
                        padding: 8px;
                    }
                """
        for btn in [self.btn_delete, self.btn_clear, self.btn_import_csv]:
            btn.setStyleSheet(button_style)

        buttons_layout.addWidget(self.btn_delete)
        buttons_layout.addWidget(self.btn_clear)
        buttons_layout.addWidget(self.btn_import_csv)
        buttons_layout.addStretch()

        buttons_group.setLayout(buttons_layout)

        # Центральная панель

        self.preview_widget = PreviewWidget()

        # Правая панель

        zoom_group = QGroupBox("Масштаб")

        zoom_layout = QVBoxLayout()

        self.lbl_zoom = QLabel("100 %")
        self.lbl_zoom.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider_zoom = QSlider(Qt.Orientation.Vertical)

        self.slider_zoom.setMinimum(50)
        self.slider_zoom.setMaximum(500)
        self.slider_zoom.setValue(100)

        zoom_layout.addWidget(self.lbl_zoom)
        zoom_layout.addWidget(self.slider_zoom)

        zoom_group.setLayout(zoom_layout)

        splitter.addWidget(buttons_group)
        splitter.addWidget(self.preview_widget)
        splitter.addWidget(zoom_group)

        splitter.setSizes([250, 900, 150])

        vertical_splitter = QSplitter(
            Qt.Orientation.Vertical
        )

        # ==================================================
        # История
        # ==================================================

        history_group = QGroupBox("История")

        history_layout = QVBoxLayout()

        self.table_history = QTableWidget()

        header = self.table_history.horizontalHeader()

        header.setStretchLastSection(False)
        header.setSectionsMovable(False)
        header.setCascadingSectionResizes(False)

        self.table_history.setColumnCount(3)
        self.table_history.setHorizontalHeaderLabels(
            ["id", "Данные", "Комментарий"]
        )

        header = self.table_history.horizontalHeader()

        header = self.table_history.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.Stretch
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents
        )

        history_layout.addWidget(self.table_history)

        history_group.setLayout(history_layout)

        vertical_splitter.addWidget(splitter)

        vertical_splitter.addWidget(history_group)

        vertical_splitter.setSizes([
            550,
            400
        ])

        main_layout.addWidget(vertical_splitter)

    def apply_dark_theme(self):
        """Применяет тёмную тему из отдельного модуля."""
        self.setStyleSheet(get_dark_stylesheet())

    def connect_signals(self):
        self.input_panel.txt_data.textChanged.connect(
            self.on_text_changed
        )

        self.slider_zoom.valueChanged.connect(
            self.on_zoom_changed
        )

        self.input_panel.btn_add.clicked.connect(
            self.on_add_clicked
        )

        self.btn_delete.clicked.connect(
            self.on_delete_clicked
        )

        self.btn_clear.clicked.connect(
            self.on_clear_clicked
        )

        self.btn_import_csv.clicked.connect(
            self.on_import_csv_clicked
        )

        self.table_history.currentCellChanged.connect(
            self.on_history_current_changed
        )

        self.table_history.itemChanged.connect(
            self.on_history_item_changed
        )

    def on_history_item_changed(self, item):

        row = item.row()

        # Изменили данные
        if item.column() == 1:
            display_text = item.text()
            storage_text = Validator.normalize_for_storage(display_text)

            if self.history.update(row, storage_text):
                if row == self.table_history.currentRow():
                    self.input_panel.txt_data.setText(display_text)  # показываем с GS
            else:
                self.update_history_table()
                self.statusBar().showMessage("Такая запись уже существует", 3000)
            return

        # Изменили комментарий
        if item.column() == 2:
            self.history.update_comment(
                row,
                item.text()
            )

            self.statusBar().showMessage(
                "Комментарий сохранён",
                1500
            )

    def on_text_changed(self):
        # Получаем то, что сейчас в поле
        current_text = self.input_panel.txt_data.text()

        # Преобразуем реальный GS в видимый "GS"
        display_text = Validator.normalize_for_display(current_text)

        # Если была замена — обновляем поле
        if display_text != current_text:
            cursor_pos = self.input_panel.txt_data.cursorPosition()
            self.input_panel.txt_data.setText(display_text)
            self.input_panel.txt_data.setCursorPosition(cursor_pos)

        # Для хранения и генерации используем реальный символ
        storage_text = Validator.normalize_for_storage(display_text)

        if not self.validate_input(storage_text):
            self.preview_widget.set_pixmap(None)
            return

        # === Цветовое выделение GS ===
        if 'GS' in display_text:
            self.input_panel.txt_data.setStyleSheet("""
                QLineEdit {
                    background-color: #1e3a2f;
                    color: #aaffaa;
                    border: 1px solid #4ade80;
                    font-weight: bold;
                }
            """)
            self.input_panel.txt_data.setToolTip("Содержит символ GS (Group Separator \\x1D)")
        else:
            self.input_panel.txt_data.setStyleSheet("")

        # Генерация
        image = self.generator.generate(storage_text)
        if image:
            self.preview_widget.set_pixmap(image)

    def validate_input(self, text: str) -> bool:
        """Проверяет данные. Не сбрасывает стиль GS при успешной валидации."""

        if not Validator.validate_data(text):
            self.input_panel.txt_data.setStyleSheet(
                "border: 2px solid red;"
            )
            return False

        # Успешная валидация — НЕ сбрасываем стиль полностью!
        # (выделение GS будет управляться в on_text_changed)
        return True

    def on_zoom_changed(self, value):

        self.lbl_zoom.setText(
            f"{value} %"
        )

        self.preview_widget.set_scale(
            value
        )

    def on_add_clicked(self):

        display_text = self.input_panel.txt_data.text()
        # Преобразуем отображаемый текст обратно в реальный (с GS)
        storage_text = Validator.normalize_for_storage(display_text)

        if not self.validate_input(storage_text):
            return

        if self.history.add(storage_text):
            self.update_history_table()
            self.statusBar().showMessage("Запись добавлена", 3000)
        else:
            self.statusBar().showMessage("Такая запись уже существует", 3000)

    def on_delete_clicked(self):

        row = self.table_history.currentRow()

        if row < 0:
            return

        self.history.remove(row)

        self.update_history_table()

        self.statusBar().showMessage(
            "Запись удалена",
            3000
        )

    def on_clear_clicked(self):

        answer = QMessageBox.question(

            self,

            "Очистка истории",

            "Удалить всю историю?",

            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No

        )

        if answer == QMessageBox.StandardButton.Yes:
            self.history.clear()

            self.update_history_table()

            self.statusBar().showMessage(
                "История очищена",
                3000
            )

    def on_import_csv_clicked(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Импорт CSV",
            "",
            "CSV (*.csv);;Все файлы (*)"
        )

        if not file_name:
            return

        try:

            records = CsvImporter.import_file(file_name)

        except Exception as error:

            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось открыть файл.\n\n{error}"
            )

            return

        imported = 0
        skipped = 0

        for record in records:

            if self.history.add(
                    record["data"],
                    record["comment"]
            ):
                imported += 1
            else:
                skipped += 1

        self.update_history_table()

        self.statusBar().showMessage(
            f"Импортировано: {imported}   Пропущено: {skipped}",
            5000
        )

    def update_history_table(self):

        self.table_history.blockSignals(True)

        records = self.history.get_all()

        self.table_history.setRowCount(len(records))

        for row, record in enumerate(records):
            self.table_history.setItem(row, 0, QTableWidgetItem(str(row + 1)))

            # Отображаем GS как текст "GS"
            display_data = Validator.normalize_for_display(record["data"])
            self.table_history.setItem(
                row, 1, QTableWidgetItem(display_data)
            )

            self.table_history.setItem(
                row, 2, QTableWidgetItem(record.get("comment", ""))
            )

        self.table_history.resizeColumnsToContents()

        header = self.table_history.horizontalHeader()

        free_space = (
                self.table_history.viewport().width()
                - self.table_history.columnWidth(0)
                - self.table_history.columnWidth(2)
        )

        if free_space > self.table_history.columnWidth(1):
            self.table_history.setColumnWidth(1, free_space)

        self.table_history.blockSignals(False)

    def on_history_current_changed(
            self,
            current_row,
            current_column,
            previous_row,
            previous_column
    ):

        if current_row < 0:
            return

        records = self.history.get_all()

        if current_row >= len(records):
            return

        self.input_panel.txt_data.setText(
            records[current_row]["data"]
        )

        self.statusBar().showMessage(
            "Данные загружены из истории",
            3000
        )