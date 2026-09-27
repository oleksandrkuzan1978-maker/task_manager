#!/usr/bin/env python
"""Точка входа для выполнения административных команд Django."""
import os
import sys


def main():
    """Выполнить команду Django, переданную в аргументах командной строки.

    Использует config.settings, если DJANGO_SETTINGS_MODULE не задан
    в окружении, и передает sys.argv диспетчеру команд Django.

    Raises:
        ImportError: Если не удалось импортировать диспетчер команд Django.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
