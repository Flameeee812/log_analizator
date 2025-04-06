import logging
from collections import defaultdict
from typing import Dict

from log_analyzer.core import load_log_file
from log_analyzer.utils import fetch_endpoint, fetch_log_level
from log_analyzer.core.exceptions import FileLoadError


def analyze_logs(*args: str) -> Dict[str, Dict[str, int]]:
    """
    Создаёт словарь API-ручек с уровнями логирования и подсчитывает количество логов каждого уровня.

    Параметры:
     - *args (str): Пути к лог-файлам, которые нужно обработать.

    Возвращаемое значение:
     - report (Dict[str, Dict[str, int]]): Словарь, где ключ — API-ручка,
       а значение — словарь с количеством логов для каждого уровня логирования.

    Исключения:
     - FileLoadError: В случае ошибки загрузки файла, ошибка логируется,
       и обработка продолжается для остальных файлов.
    """

    # Инициализация отчёта с нулевыми значениями для каждого уровня логирования
    report = defaultdict(lambda: {"DEBUG": 0, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0})

    for log_file in args:
        try:
            logs = load_log_file(log_file)

            for log in logs:
                # Извлечение уровня логирования и endpoint-а из строки лога
                log_level: str = fetch_log_level(log.split())
                endpoint: str = fetch_endpoint(log.split())

                # Если оба значения присутствуют, обновляем статистику
                if log_level and endpoint:
                    report[endpoint][log_level] += 1

        except FileLoadError as e:
            logging.error(f"Ошибка обработки файла '{log_file}': {e}")
            continue

    return dict(report)


def count_total_log_levels(report: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    """
    Подсчитывает общее количество логов для каждого уровня логирования.

    Параметры:
     - report (Dict[str, Dict[str, int]]): Словарь, где ключи — API-ручки,
       а значения — словари с уровнями логирования.

    Возвращаемое значение:
     - total (Dict[str, int): Словарь с количеством логов для каждого уровня логирования.
    """

    # Инициализация словаря для подсчёта всех уровней логирования
    total = {key: 0 for key in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]}

    # Подсчёт всех логов по уровням
    for levels in report.values():
        for key in total:
            total[key] += levels[key]

    return total


def count_total_requests(report: Dict[str, int]) -> int:
    """
    Подсчитывает общее количество запросов для всех уровней логирования.

    Параметры:
     - report (Dict[str, int]): Словарь, где ключ — это API-ручка,
       а значения — словари с уровнями логирования.

    Возвращаемое значение:
     - total_request (int): общее количество запросов.
    """

    return sum(report.values())
