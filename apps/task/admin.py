"""Регистрация моделей задач, подзадач и категорий в админке Django."""

from django.contrib import admin
from .models import Task, SubTask, Category

# Register your models here.

# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)

#
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Отображать название и время создания задачи в списке админки."""

    list_display = ('title', 'created_at')


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    """Отображать название и время создания подзадачи в списке админки."""

    list_display = ('title', 'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображать имя категории в списке админки."""

    list_display = ('name',)