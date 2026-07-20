from pathlib import Path
import sys


def get_app_path(*parts: str) -> Path:
    """
    Возвращает путь к файлу внутри каталога приложения
    как при запуске из исходников, так и после сборки PyInstaller.
    """

    if getattr(sys, "frozen", False):
        base_path = Path(sys.executable).resolve().parent

        resource_path = base_path.joinpath(*parts)
        if resource_path.exists():
            return resource_path

        return base_path.joinpath("_internal", *parts)

    return Path(__file__).resolve().parents[1].joinpath(*parts)