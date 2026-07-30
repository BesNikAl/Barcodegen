from core.datamatrix_generator import DataMatrixGenerator
from core.history_manager import HistoryManager
from core.csv_importer import CsvImporter
from core.validator import Validator
from ui.widgets.input_panel import InputPanel
from ui.widgets.preview_widget import PreviewWidget
from ui.widgets.zoom_panel import ZoomPanel
from ui.widgets.history_table import HistoryTable
from ui.styles.dark_theme import get_dark_stylesheet
from core.settings import get_app_path
from pathlib import Path
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGroupBox,
    QSplitter,
    QMessageBox,
    QFileDialog,
)


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

        self.zoom_panel = ZoomPanel()

        splitter.addWidget(buttons_group)
        splitter.addWidget(self.preview_widget)
        splitter.addWidget(self.zoom_panel)

        splitter.setSizes([250, 900, 150])

        vertical_splitter = QSplitter(
            Qt.Orientation.Vertical
        )

        # ==================================================
        # История
        # ==================================================

        self.history_table = HistoryTable()

        vertical_splitter.addWidget(splitter)

        vertical_splitter.addWidget(self.history_table)

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

        self.zoom_panel.zoom_changed.connect(
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

        self.history_table.current_row_changed.connect(
            self.on_history_current_changed
        )
        self.history_table.data_edited.connect(
            self.on_history_data_edited
        )
        self.history_table.comment_edited.connect(
            self.on_history_comment_edited
        )

    def on_history_data_edited(self, row: int, display_text: str):
        storage_text = Validator.normalize_for_storage(display_text)

        if self.history.update(row, storage_text):
            if row == self.history_table.current_row():
                self.input_panel.txt_data.setPlainText(display_text)
        else:
            self.update_history_table()
            self.statusBar().showMessage("Такая запись уже существует", 3000)

    def on_history_comment_edited(self, row: int, comment: str):
        self.history.update_comment(row, comment)
        self.statusBar().showMessage("Комментарий сохранён", 1500)

    def on_text_changed(self):

        text = self.input_panel.txt_data.text()

        if not self.validate_input(text):
            # Очищаем предпросмотр при некорректных данных
            self.preview_widget.set_pixmap(None)
            return

        image = self.generator.generate(text)

        if image:
            self.preview_widget.set_pixmap(image)

    def validate_input(self, text: str):

        if not Validator.validate_data(text):
            self.input_panel.txt_data.setStyleSheet(
                "border: 2px solid red;"
            )
            return False

        self.input_panel.txt_data.setStyleSheet("")
        return True

    def on_zoom_changed(self, value: int):
        self.preview_widget.set_scale(value)

    def on_add_clicked(self):

        text = self.input_panel.txt_data.text()

        if not self.validate_input(text):
            return

        if self.history.add(text):

            self.update_history_table()

            self.statusBar().showMessage(
                "Запись добавлена",
                3000
            )

        else:

            self.statusBar().showMessage(
                "Такая запись уже существует",
                3000
            )

    def on_delete_clicked(self):

        row = self.history_table.current_row()

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
        self.history_table.update_records(self.history.get_all())

    def on_history_current_changed(self, current_row: int):
        if current_row < 0:
            return

        records = self.history.get_all()
        if current_row >= len(records):
            return

        display_data = Validator.normalize_for_display(
            records[current_row]["data"]
        )
        self.input_panel.txt_data.setPlainText(display_data)

        self.statusBar().showMessage(
            "Данные загружены из истории",
            3000
        )