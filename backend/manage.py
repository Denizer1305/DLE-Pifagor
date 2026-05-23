#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

from __future__ import annotations

import os
import sys


def main():
    """
    Запускает административные команды Django.

    По умолчанию используется локальное окружение проекта.
    Для production/test окружений DJANGO_SETTINGS_MODULE можно переопределить
    через переменную окружения.
    """

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Вы уверены, что он установлен и "
            "доступен в вашей переменной среды PYTHONPATH? Вы "
            "забыли активировать виртуальную среду?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
