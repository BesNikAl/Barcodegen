# BarcodeGen

## Общая информация

Название проекта: BarcodeGen

Версия проекта: 0.4.5

Платформа:
- Windows 10
- Windows 11

Язык:
- Python 3.12+

GUI:
- PyQt6

IDE:
- PyCharm Professional

Тип проекта:
Коммерческое настольное приложение.

Главная цель:
Создать полноценный аналог Barcode Studio с возможностью генерации различных типов штрихкодов.

---

# Уже реализовано

На текущем этапе реализовано:

✔ Генерация DataMatrix ECC200

✔ Предпросмотр с возможностью масштабирования

✔ История с сохранением в history.json

✔ Тёмная тема (Dark Theme)

✔ Импорт истории из CSV:

✔ Поддерживаются файлы с одной колонкой (data) и двумя колонками (data, comment)

✔ Автоматическое определение разделителя

✔ Поддержка UTF-8 и UTF-8 BOM

✔ Пропуск дубликатов и некорректных записей

✔ Статистика импортированных и пропущенных записей в строке состояния

✔ Интерфейс: InputPanel, PreviewWidget, HistoryManager

✔ Комментарии к записям истории (колонка «Комментарий» вместо «Дата»)

---

# Планируемые функции

- Типы штрихкодов: QR, Code128, EAN13, GS1 DataMatrix

- Импорт: TXT, Excel

- Экспорт: PDF, PNG, SVG, BMP

- Дополнительно: Настройки, Выбор темы, Печать, Настройка размеров модулей, Генерация серий, Предпросмотр печати, Windows Installer

---

## Правила сборки проекта

### Сборка

Для сборки используется **PyInstaller**.

В проекте единственным источником конфигурации сборки является файл:

```
BarcodeGen.spec
```

Файл `build.bat` используется только как оболочка для запуска сборки и не должен содержать параметры PyInstaller, дублирующие `.spec`.

Все изменения параметров сборки (ресурсы, DLL, скрытые импорты, иконка, режим сборки и т.д.) вносятся только в `BarcodeGen.spec`.

---

### build.bat

Скрипт выполняет следующие действия:

1. Удаляет временную папку `build`;
2. Удаляет предыдущую сборку `dist`;
3. Запускает `BarcodeGen.spec`;
4. Отображает результат сборки.

---

### Структура готовой сборки

При использовании режима `--onedir` готовым приложением считается вся папка:

```
dist/
    BarcodeGen/
```

Именно эта папка предназначена для:

* распространения;
* архивирования;
* копирования на другой компьютер;
* публикации релизов.

Файл `BarcodeGen.exe` не предназначен для использования отдельно, так как зависит от расположенных рядом библиотек и ресурсов.

---

### Структура проекта

```
BarcodeGen/
├── main.py                 # Точка входа
├── core/                   # Бизнес-логика (не зависит от PyQt)
│   ├── __init__.py
│   ├── csv_importer.py     # Импорт из CSV
│   ├── datamatrix_generator.py
│   ├── history_manager.py
│   ├── pdf_exporter.py
│   ├── settings.py
│   └── validator.py
├── ui/                     # Пользовательский интерфейс
│   ├── __init__.py
│   ├── main_window.py
│   └── widgets/
│       ├── __init__.py
│       ├── history_table.py
│       ├── info_panel.py
│       ├── input_panel.py
│       ├── preview_widget.py
│       └── zoom_panel.py
│   ├── styles/
│       └── dark_theme.py
├── resources/              # Иконки, шрифты, изображения
│   ├── fonts
│   ├── icons
│   └── images
├── data/
│   └── history.json        # Файл истории
├── logs/
├── docs/
│   └──CHANGELOG.md
├── build.bat               # Скрипт сборки
├── BarcodeGen.spec         # Конфигурация PyInstaller
├── README.md
└── requirements.txt
```

Все пользовательские данные должны храниться рядом с приложением и не требовать установки дополнительных компонентов.

---

# Архитектура

Следовать SOLID.

Один класс = один файл.

Минимум логики в MainWindow.

GUI никогда не содержит бизнес-логику.

Бизнес-логика никогда не зависит от PyQt.

Все взаимодействие осуществляется через отдельные классы.

---

# Ответственность классов

MainWindow

Отвечает только за:

- построение окна
- соединение сигналов
- взаимодействие между компонентами

Не содержит:

- генерацию
- работу с JSON
- экспорт
- проверку данных

---

InputPanel

Отвечает только за ввод текста.

---

PreviewWidget

Отвечает только за отображение изображения.

Хранит:

- исходный QPixmap
- масштаб

Сам выполняет масштабирование.

---

InfoPanel

Отображает информацию:

- количество символов
- размер матрицы
- размер символа

---

HistoryTable

Отвечает только за отображение истории.

Не работает напрямую с JSON.

---

HistoryManager

Работает исключительно с history.json.

Должен содержать методы:

- load()
- save()
- add()
- remove()
- clear()
- update()
- get_all()

---

Validator

Отвечает исключительно за проверку данных.

На текущем этапе:

- максимум 500 символов
- запрет кириллицы
- запрет дубликатов

Позже:

- GS1
- QR
- Code128
- другие ограничения

---

DataMatrixGenerator

Отвечает только за генерацию ECC200.

Не знает ничего про GUI.

В будущем должен возвращать PIL.Image.

Конвертация PIL → QPixmap выполняется только в PreviewWidget.

---

# Правила разработки

Каждый класс располагается в отдельном файле.

Каждый файл имеет одинаковую структуру.

Initialization

UI

Signals

Slots

Private methods

---

# Правила изменения существующего кода

Никогда не переписывать файл полностью без необходимости.

Если изменение небольшое:

1. объяснить зачем оно нужно

2. показать какой код найти

3. показать чем заменить

Если изменение превышает примерно 100 строк — допускается заменить файл полностью.

После каждого этапа приложение должно запускаться.

Не выполнять большой рефакторинг.

Все изменения должны быть локальными.

---

# Правила архитектуры

Не использовать глобальные переменные.

Максимально использовать type hints.

Избегать магических чисел.

Использовать именованные константы.

Использовать logging.

Использовать pathlib.

Не создавать циклических импортов.

---

# Правила GUI

Dark Theme.

Использовать StyleSheet.

В дальнейшем тема переносится в

ui/styles/dark_theme.py

---

# Правила таблицы истории

История хранится в history.json.

При запуске автоматически загружается.

Редактируемым является только столбец "Данные".

Столбцы "№" и "Дата" доступны только для чтения.

При выборе строки:

- одинарный клик обновляет DataMatrix
- клавиши ↑ ↓ обновляют DataMatrix

Редактирование строки обновляет:

- history.json
- Preview
- InputPanel

Дубликаты запрещены.

---

# Правила Preview

DataMatrix отображается всегда один.

Изменение масштаба изменяет только отображение.

Исходное изображение никогда не пересоздается.

---

# Сборка

Используется PyInstaller.

Использовать onedir.

Использовать BarcodeGen.spec.

Автоматически подключать

- libdmtx-64.dll
- history.json
- resources

---

# Что НЕ делать

Не менять архитектуру без обсуждения.

Не выполнять неожиданный рефакторинг.

Не переносить код между файлами без необходимости.

Не менять публичные интерфейсы классов без обсуждения.

---

# Что желательно улучшить

После завершения текущего функционала:

1.
Вынести Validator в отдельный класс.

2.
Разделить MainWindow.

3.
Добавить logging.

4.
Добавить Settings.

5.
Перевести генератор на возврат PIL.Image.

6.
Вынести тему в отдельный файл.

---

## Ссылки на исходные файлы

- [`main.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/main.py)
- [`BarcodeGen.spec`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/BarcodeGen.spec)
- [`build.bat`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/build.bat)
- [`requirements.txt`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/requirements.txt)
- **core/**
  - [`__init__.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/core/__init__.py)
  - [`csv_importer.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/core/csv_importer.py)
  - [`datamatrix_generator.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/core/datamatrix_generator.py)
  - [`history_manager.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/core/history_manager.py)
  - [`pdf_exporter.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/core/pdf_exporter.py)
  - [`settings.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/core/settings.py)
  - [`validator.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/core/validator.py)
- **docs/**
  - [`CHANGELOG.md`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/docs/CHANGELOG.md)
- **ui/**
  - [`main_window.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/ui/main_window.py)
  - [`__init__.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/ui/__init__.py)
  - **widgets/**
    - [`__init__.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/ui/widgets/__init__.py)
    - [`history_table.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/ui/widgets/history_table.py)
    - [`info_panel.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/ui/widgets/info_panel.py)
    - [`input_panel.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/ui/widgets/input_panel.py)
    - [`preview_widget.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/ui/widgets/preview_widget.py)
    - [`zoom_panel.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/ui/widgets/zoom_panel.py)
  - **styles/**
    - [`dark_theme.py`](https://raw.githubusercontent.com/BesNikAl/Barcodegen/refs/heads/master/ui/styles/dark_theme.py)
