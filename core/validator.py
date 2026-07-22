import re


class Validator:
    """Отвечает исключительно за проверку данных."""

    MAX_LENGTH = 500
    CYRILLIC_PATTERN = re.compile(r"[А-Яа-яЁё]")

    @staticmethod
    def validate_data(text: str) -> bool:
        """
        Проверяет данные для DataMatrix.
        Возвращает True, если данные корректны.
        """
        if len(text) > Validator.MAX_LENGTH:
            return False

        if Validator.CYRILLIC_PATTERN.search(text):
            return False

        return True