def get_dark_stylesheet() -> str:
    """Возвращает stylesheet для тёмной темы."""
    return """
        QWidget {
            background-color: #252525;
            color: white;
            font-size: 10pt;
        }

        QGroupBox {
            border: 1px solid #444;
            margin-top: 8px;
            padding-top: 10px;
        }

        QLineEdit {
            background-color: #303030;
            border: 1px solid #555;
            padding: 6px;
        }

        QPushButton {
            background-color: #D32F2F;
            border: none;
            padding: 8px;
            border-radius: 6px;
        }

        QPushButton:hover {
            background-color: #E53935;
        }

        QTableWidget {
            background-color: #303030;
            gridline-color: #444;
        }

        QHeaderView::section {
            background-color: #404040;
            padding: 5px;
        }

        QSlider {
            /* Дополнительно для слайдера масштаба */
        }
    """