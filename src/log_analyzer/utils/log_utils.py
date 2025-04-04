from typing import Optional


def fetch_endpoint(split_log: list) -> str:
    """
    Функция для возврата API-ручки
    """

    for part in split_log:
        if part.startswith("/") and part.endswith("/"):
            return part


def fetch_log_level(split_log: list) -> Optional[str]:
    """
    Функция для возврата уровеня логирования лог-строки.
    """

    for part in split_log:
        if part in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            return part
