import logging

from src.log_analyzer.cli import initialize_parser


if __name__ == "__main__":
    # Настройка логирования
    logging.basicConfig(level=logging.WARNING)

    # Инициализация парсера аргументов командной строки
    parser = initialize_parser()

    args = parser.parse_args()

    # Проверка наличия аргумента 'log_files'
    if not args.log_files:
        parser.print_help()
        exit(1)

    # Обработка отчёта в зависимости от '--report'
    if args.report is not None:
        # Сохранение отчёта в файл
        args.save_report_to_txt(args.report, *args.log_files)

    else:
        # Вывод отчёта в консоль
        args.print_report_func(*args.log_files)

