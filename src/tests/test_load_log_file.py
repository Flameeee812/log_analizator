from typing import Iterator

import pytest

from log_analyzer.core import load_log_file
from log_analyzer.core.exceptions import FileLoadError


@pytest.fixture
def valid_file() -> str:
    """
    Фикстура, которая возвращает путь к существующему лог-файлу для тестов.

    Возвращаемое значение:
     - str: Путь к лог-файлу, который существует.
    """
    return "logs/app1.log"


@pytest.fixture
def empty_file() -> str:
    """
    Фикстура, которая возвращает путь к пустому лог-файлу для тестов.

    Возвращаемое значение:
     - str: Путь к лог-файлу, который не содержит строк (пустой файл).
    """
    return "logs/empty_log.log"


@pytest.fixture
def invalid_file() -> str:
    """
    Фикстура, которая возвращает путь к несуществующему лог-файлу для тестов.

    Возвращаемое значение:
     - str: Путь к лог-файлу, который не существует и вызовет ошибку при попытке его загрузить.
    """
    return "logs/app1.lo"


def test_returns_iterator(valid_file):
    """
    Проверяет, что функция load_log_file возвращает итератор.

    Параметры:
     - valid_file (str): Путь к корректному лог-файлу.

    Ожидаемый результат:
     - Проверка того, что возвращаемое значение является объектом Iterator.
    """
    test_file = load_log_file(valid_file)

    assert isinstance(test_file, Iterator)


def test_returns_log_lines(valid_file):
    """
    Проверяет, что функция load_log_file возвращает строки.

    Параметры:
     - valid_file (str): Путь к лог-файлу с данными.

    Ожидаемый результат:
     - Проверка того, что функция возвращает лог-строки.
    """

    test_file = load_log_file(valid_file)
    for test_line in test_file:
        assert isinstance(test_line, str)


def test_log_line_format(valid_file):
    """
    Проверяет, что строка из лога имеет правильный формат.

    Параметры:
     - valid_file (str): Путь к лог-файлу с данными.

    Ожидаемый результат:
     - Проверка того, что функция возвращает лог-строки правильного формата.
        """

    test_file = load_log_file(valid_file)
    test_line = next(test_file).split()

    assert len(test_line) >= 4
    assert test_line[2] in ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]


def test_empty_log_file(empty_file):
    """
    Проверяет, что функция load_log_file вызывает StopIteration для пустого лог-файла.

    Параметры:
     - empty_file (str): Путь к пустому лог-файлу.

    Ожидаемый результат:
     - Проверка того, что при чтении из пустого файла генерируется исключение StopIteration.
    """
    test_file = load_log_file(empty_file)

    with pytest.raises(StopIteration):
        next(test_file)


def test_invalid_log_file(invalid_file):
    """
    Проверяет, что функция load_log_file вызывает исключение FileLoadError для несуществующего файла.

    Параметры:
        invalid_file (str): Путь к несуществующему лог-файлу.

    Ожидаемый результат:
        Проверка того, что при попытке загрузить несуществующий файл генерируется исключение FileLoadError.
    """

    test_file = load_log_file(invalid_file)

    with pytest.raises(FileLoadError):
        next(test_file)
