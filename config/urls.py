"""Корневые маршруты проекта.

Список urlpatterns подключает административный интерфейс по пути admin/.
"""
from django.contrib import admin
from django.urls import path
from apps.task import views
urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('create/', views.create_task, name="create_task"),
    path('tasks/',views.get_all_tasks, name="get_all_tasks"),
    path('tasks/<int:id>/', views.get_one_task, name="get_one_task"),
    path('tasks/aggregate/', views.get_task_count, name="get_task_count"),
    path('cat/<int:id>/', views.update_category, name="update_category"),
]
