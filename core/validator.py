import re


class Validator:
    """Отвечает исключительно за проверку данных."""

    MAX_LENGTH = 500
    CYRILLIC_PATTERN = re.compile(r"[А-Яа-яЁё]")

    @staticmethod
    def validate_data(text: str) -> bool:
        """
        Проверяет данные для DataMatrix.
        GS (\\x1D) разрешён.
        Возвращает True, если данные корректны.
        """
        if len(text) > Validator.MAX_LENGTH:
            return False

        if Validator.CYRILLIC_PATTERN.search(text):
            return False

        return True

    GS_CHAR = '\x1D'
    GS_DISPLAY = 'GS'

    @staticmethod
    def normalize_for_display(text: str) -> str:
        """Заменяет GS на видимый 'GS' для UI."""
        return text.replace(Validator.GS_CHAR, Validator.GS_DISPLAY)

    @staticmethod
    def normalize_for_storage(text: str) -> str:
        """Заменяет отображаемый 'GS' обратно на реальный символ."""
        return text.replace(Validator.GS_DISPLAY, Validator.GS_CHAR)