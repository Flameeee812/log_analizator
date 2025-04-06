import pytest

from log_analyzer.utils import fetch_endpoint, fetch_log_level


@pytest.fixture()
def log_line_with_endpoint() -> list[str]:
    """
    Фикстура для получения разбитой строки из лог-файла с endpoint'ом.

    Возвращаемое згачение:
     - list[str]: Список слов, полученных из первой строки лог-файла.
    """

    log_line = "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]"

    return log_line.split()


@pytest.fixture()
def log_line_without_endpoint() -> list[str]:
    """
    Фикстура для получения разбитой строки без endpoint'а.

    Возвращаемое значение:
     - list[str]: Список слов из строки лога без API-запроса.
    """

    log_line = "2025-03-28 12:40:47,000 CRITICAL django.core.management: DatabaseError: Deadlock detected"

    return log_line.split()


@pytest.fixture()
def empty_log_line() -> list[str]:
    """
    Фикстура для получения пустой строки из лога.

    Возвращаемое значение:
     - empty_line (list[str]): Пустой список
    """

    empty_line = " "

    return empty_line.split()


def test_fetch_endpoint(log_line_with_endpoint, log_line_without_endpoint, empty_log_line):
    """
    Проверяет, что функция fetch_endpoint корректно извлекает endpoint из лог-строки.
    """

    endpoint_log_line: list = log_line_with_endpoint  # Корректная лог-строка с endpoint'ом в теле
    non_endpoint_log_line: list = log_line_without_endpoint  # Лог-строка буз endpoint'а в теле
    empty_line: list = empty_log_line  # Пустая строка

    assert fetch_endpoint(endpoint_log_line) == "/api/v1/reviews/"
    assert fetch_endpoint(non_endpoint_log_line) is None
    assert fetch_endpoint(empty_line) is None


def test_fetch_log_level(log_line_with_endpoint, log_line_without_endpoint, empty_log_line):
    """
    Проверяет, что функция fetch_log_level корректно извлекает уровень логирования.
    """

    endpoint_log_line: list = log_line_with_endpoint  # Корректная лог-строка с endpoint'ом в теле
    non_endpoint_log_line: list = log_line_without_endpoint  # Лог-строка буз endpoint'а в теле
    empty_line: list = empty_log_line  # Пустая строка

    assert fetch_log_level(endpoint_log_line) == "INFO"
    assert fetch_endpoint(non_endpoint_log_line) is None
    assert fetch_endpoint(empty_line) is None
