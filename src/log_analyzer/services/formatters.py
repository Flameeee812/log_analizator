from typing import Dict


def format_report(report: Dict[str, Dict[str, int]], total: Dict[str, int], total_requests: int) -> str:
    """
    Форматирует отчет для вывода или записи в файл.

    Параметры:
     - report (Dict[str, Dict[str, int]]): Словарь с подсчитанными логами.
     - total (Dict[str, int]): Словарь с итоговыми подсчетами для всех уровней.
     - total_requests int: Общее количество запросов.

    Возвращаемое значение:
     - formatted_report (str): Строка с отформатированным отчетом.
    """

    # список с названиями заголовков
    headers = ["HANDLER", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    report_lines = [
        # Добавляем строку 'Total requests'
        f"Total requests: {total_requests}\n",
        # Добавляем строку с заголовками
        f"{headers[0]:<30} {headers[1]:<15} {headers[2]:<15} {headers[3]:<15} {headers[4]:<15} {headers[5]:<15}",
        "-" * 100
    ]

    # Добавляем данные по каждому endpoint
    for endpoint, levels in report.items():
        report_lines.append(f"{endpoint:<30}"
                            f"{levels['DEBUG']:<15}"
                            f"{levels['INFO']:<15}"
                            f"{levels['WARNING']:<15}"
                            f"{levels['ERROR']:<15}"
                            f"{levels['CRITICAL']:<15}")
    report_lines.append("-" * 100)

    # Добавляем итоговую строку с общим количеством логов по уровням
    report_lines.append(f"{'Total':<30}"
                        f"{total['DEBUG']:<15}"
                        f"{total['INFO']:<15}"
                        f"{total['WARNING']:<15}"
                        f"{total['ERROR']:<15}"
                        f"{total['CRITICAL']:<15}")

    return "\n".join(report_lines)
