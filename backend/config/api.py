"""
Вспомогательные функции для чтения переменных окружения.

Модуль также пытается загрузить корневой .env-файл, если установлен
python-dotenv. Это удобно для локальной разработки без docker-compose.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
ENV_FILE = PROJECT_ROOT / ".env"

if load_dotenv is not None and ENV_FILE.exists():
    load_dotenv(ENV_FILE)


def get_env(name: str, default: Any = None, *, required: bool = False) -> str | Any:
    """
    Возвращает значение переменной окружения.

    Args:
        name:
            Название переменной окружения.
        default:
            Значение по умолчанию.
        required:
            Если True, отсутствие переменной вызовет RuntimeError.

    Returns:
        str | Any: Значение переменной окружения или default.

    Raises:
        RuntimeError: Если переменная обязательна, но не задана.
    """

    value = os.environ.get(name, default)

    if required and value in (None, ""):
        raise RuntimeError(f"Environment variable {name} is required.")

    return value


def get_bool_env(name: str, default: bool = False) -> bool:
    """
    Возвращает boolean-значение из переменной окружения.

    Args:
        name:
            Название переменной окружения.
        default:
            Значение по умолчанию.

    Returns:
        bool: Приведённое boolean-значение.
    """

    value = os.environ.get(name)

    if value is None:
        return default

    return value.strip().lower() in {"true", "1", "yes", "y", "on"}


def get_int_env(name: str, default: int) -> int:
    """
    Возвращает integer-значение из переменной окружения.

    Args:
        name:
            Название переменной окружения.
        default:
            Значение по умолчанию.

    Returns:
        int: Приведённое integer-значение.

    Raises:
        RuntimeError: Если значение невозможно привести к int.
    """

    value = os.environ.get(name)

    if value is None:
        return default

    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be integer.") from exc


def get_list_env(
    name: str,
    default: list[str] | None = None,
    *,
    separator: str = ",",
) -> list[str]:
    """
    Возвращает список строк из переменной окружения.

    Args:
        name:
            Название переменной окружения.
        default:
            Значение по умолчанию.
        separator:
            Разделитель элементов.

    Returns:
        list[str]: Список значений.
    """

    value = os.environ.get(name)

    if value is None:
        return default or []

    return [item.strip() for item in value.split(separator) if item.strip()]


def get_path_env(name: str, default: Path) -> Path:
    """
    Возвращает путь из переменной окружения.

    Args:
        name:
            Название переменной окружения.
        default:
            Значение по умолчанию.

    Returns:
        Path: Объект Path.
    """

    value = os.environ.get(name)

    if value is None:
        return default

    return Path(value)
