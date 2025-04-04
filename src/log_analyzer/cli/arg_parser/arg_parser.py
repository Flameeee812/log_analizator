import argparse
from ..cli_commands import print_report, save_report_to_file


def initialize_parser():
    """Инициализация парсера аргументов командной строки"""

    parser = argparse.ArgumentParser(
        description="CLI-приложение для сохранения отчёта о состоянии ручек API по каждому уровню логирования."
    )

    # Основные аргументы
    parser.add_argument(
        "log_files",
        nargs="*",
        help="Пути к лог-файлам для анализа (можно указать несколько)"
    )

    parser.add_argument(
        "--report",
        help="Введите имя файла, в который хотите сохранить отчёт."
    )

    parser.set_defaults(
        print_report_func=print_report,
        save_report_to_txt=save_report_to_file
    )

    return parser
