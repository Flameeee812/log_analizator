import pytest

from log_analyzer.services.analyzers import analyze_logs, count_total_log_levels, count_total_requests
from log_analyzer.core.exceptions import FileLoadError


@pytest.fixture()
def sample_log_data():
    """
    Фикстура для примера данных, возвращаемых функцией load_log_file.

    Создаёт список строк, имитирующих записи лога. Эти данные используются
    для тестирования функции analyze_logs.

    Возвращаемое значение:
     - Список строк, представляющих логи с разными уровнями логирования.
    """
    return [
        "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]",
        "2025-03-28 12:45:46,000 ERROR django.request: POST /api/v1/reviews/ 500 Internal Server Error [192.168.1.59]",
        "2025-03-28 12:46:46,000 INFO django.request: GET /api/v1/comments/ 200 OK [192.168.1.59]",
        "2025-03-28 12:47:46,000 WARNING django.request: DELETE /api/v1/reviews/ 404 Not Found [192.168.1.59]",
    ]


def test_analyze_logs(sample_log_data, monkeypatch):
    """
    Тестирует функцию analyze_logs, которая анализирует логи и подсчитывает количество
    логов для каждого уровня логирования по API-ручкам.

    Параметры:
     - sample_log_data (list): Пример данных логов для теста.
     = monkeypatch (pytest.MonkeyPatch): Патчинг функции загрузки логов.

    Проверяется, что:
     - Результат включает нужные endpoint'ы.
     - Статистика по уровням логирования корректно подсчитывается для каждого endpoint'а.
    """

    # Подготовим фиктивные данные
    def mock_loader(_):
        return iter(sample_log_data)

    # Патчим функцию загрузки логов
    monkeypatch.setattr("log_analyzer.services.analyzers.load_log_file", mock_loader)

    # Вызов функции анализа логов
    result = analyze_logs("fakelogfile.log")

    # Проверка наличия endpoint'ов
    assert "/api/v1/reviews/" in result
    assert "/api/v1/comments/" in result

    # Проверка статистики для каждого endpoint'а
    assert result["/api/v1/reviews/"] == {
        "DEBUG": 0, "INFO": 1, "WARNING": 1, "ERROR": 1, "CRITICAL": 0
    }
    assert result["/api/v1/comments/"] == {
        "DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0
    }


def test_analyze_logs_with_load_error(sample_log_data, monkeypatch, caplog):
    """
    Тестирует обработку ошибок при загрузке логов в функции analyze_logs.

    Проверяет, что в случае ошибки загрузки файла:
     - Генерируется исключение FileLoadError.
     - Ошибка корректно логируется с правильным сообщением.

    Параметры:
     - sample_log_data (list): Пример данных логов для теста.
     - monkeypatch (pytest.MonkeyPatch): Патчинг функции загрузки логов.
     - caplog (pytest.LogCaptureFixture): Захват логов для проверки.
    """

    # Функция-замена для загрузки файлов, которая вызывает исключение
    def mock_loader_with_error(_):
        raise FileLoadError("nonexistent.log")

    # Патчим функцию загрузки логов
    monkeypatch.setattr("log_analyzer.services.analyzers.load_log_file", mock_loader_with_error)

    # Вызов функции анализа логов, который должен вызвать ошибку
    analyze_logs("nonexistent.log")

    assert "Ошибка обработки файла 'nonexistent.log': Ошибка загрузки файла: 'nonexistent.log' не найден." in caplog.text


def test_count_total_log_levels():
    """
    Тестирует функцию count_total_log_levels, которая подсчитывает количество логов для каждого уровня
    логирования в отчёте.

    Проверяется:
     - Что функция правильно суммирует количество логов для каждого уровня.
    """
    report = {
        "/api/v1/reviews/": {"DEBUG": 0, "INFO": 1, "WARNING": 1, "ERROR": 1, "CRITICAL": 0},
        "/api/v1/comments/": {"DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0},
    }

    # Вызов функции для подсчёта уровней логов
    result = count_total_log_levels(report)

    # Проверка, что подсчитанные значения правильные
    assert result == {"DEBUG": 0, "INFO": 2, "WARNING": 1, "ERROR": 1, "CRITICAL": 0}


def test_count_total_requests():
    """
    Тестирует функцию count_total_requests, которая подсчитывает общее количество всех логов.

    Проверяется:
     - Что функция правильно подсчитывает общее количество логов.
    """
    total = {
        "DEBUG": 3,
        "INFO": 1,
        "WARNING": 3,
        "ERROR": 7,
        "CRITICAL": 3
    }

    # Вызов функции для подсчёта общего количества логов
    result = count_total_requests(total)

    assert result == 17
