"""Точка входа WSGI для проекта task_manager.

Предоставляет серверу WSGI объект application. Если модуль настроек
не задан в окружении, использует config.settings.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
