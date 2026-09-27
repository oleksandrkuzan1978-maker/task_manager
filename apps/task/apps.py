"""Конфигурация приложения задач для реестра приложений Django."""

from django.apps import AppConfig


class TaskConfig(AppConfig):
    """Зарегистрировать приложение apps.task в проекте Django."""

    name = 'apps.task'
