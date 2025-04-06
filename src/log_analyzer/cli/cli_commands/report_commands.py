import logging
from log_analyzer.services import (
    format_report, count_total_log_levels, count_total_requests, analyze_logs
)


def print_report(*args: str) -> None:
    """
    Форматирует отчет о состоянии API-ручек по уровням логирования и выводит его в консоль.

    Параметры:
     - *args (str): Пути к лог-файлам для анализа (можно указать несколько).
    """

    report = analyze_logs(*args)
    total_log_levels = count_total_log_levels(report)
    total_requests = count_total_requests(total_log_levels)

    if total_requests == 0:
        print("Нет данных для отображения.")
    else:
        formatted_report = format_report(report, total_log_levels, total_requests)
        print(formatted_report)


def save_report_to_file(filename: str, *args: str) -> None:
    """
    Форматирует отчет о состоянии API-ручек по уровням логирования и сохраняет его в указанный файл.

    Параметры:
     - filename (str): Имя файла (без расширения), в который будет сохранен отчет.
     - *args (str): Пути к лог-файлам для анализа (можно указать несколько).

    Исключения:
     - В случае ошибки при записи в файл, функция логирует ошибку через модуль logging.
    """

    report = analyze_logs(*args)
    total_log_levels = count_total_log_levels(report)
    total_requests = count_total_requests(total_log_levels)

    formatted_report = format_report(report, total_log_levels, total_requests)

    try:
        with open(f"{filename}.txt", "a", encoding="utf-8") as file:
            file.write(formatted_report + "\n")
    except Exception as e:
        logging.error(f"Ошибка при сохранении отчёта в файл '{filename}.txt': {e}")
