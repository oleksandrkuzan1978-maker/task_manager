"""Корневые маршруты проекта.

Список urlpatterns подключает административный интерфейс по пути admin/.
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
