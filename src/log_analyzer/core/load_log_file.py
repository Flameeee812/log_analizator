from typing import Iterator

from log_analyzer.core.exceptions import FileLoadError


def load_log_file(path: str) -> Iterator[str]:
    """
    Функция для чтения лог-файла по указанному пути.

    Параметры:
     - path (str): Путь к лог-файлу, который необходимо загрузить.

    Возвращаемое значение:
     - Итератор строк (Iterator[str]): Итератор, который поочередно возвращает строки из лог-файла.

    Исключения:
     - FileLoadError: Выбрасывается, если файл по указанному пути не найден. В этом случае ошибка логируется.
    """

    try:
        with open(file=path, mode="r", encoding="utf-8") as file:
            for log in file:
                yield log.strip()
    except FileNotFoundError:
        raise FileLoadError(path)
