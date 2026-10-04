"""Регистрация моделей задач, подзадач и категорий в админке Django."""

from django.contrib import admin
from .models import Task, SubTask, Category
from django.utils import timezone
from django.utils.formats import date_format

# Register your models here.

# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)

#
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Отображать название и время создания задачи в списке админки."""

    list_display = ('title', 'created_at', 'deadline')
    search_fields = ('title',)
    ordering = ('-created_at',)
    fields = ('title', 'status', 'description', 'deadline')
    list_per_page = 10


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    """Отображать название и время создания подзадачи в списке админки."""

    list_display = ('title', 'task', 'created_at', 'deadline')
    search_fields = ('title', 'task__title')
    ordering = ('-created_at', 'task')
    fields = ('title', 'status', 'description', 'deadline')
    list_per_page = 10

    @admin.display(description="Срок родительской задачи")
    def task_deadline_reminder(self, obj):
        if obj is None or not obj.task_id:
            return "Срок появится после сохранения подзадачи с выбранной задачей."

        deadline = obj.task.deadline

        if deadline is None:
            return "У родительской задачи срок не указан."

        if timezone.is_aware(deadline):
            deadline = timezone.localtime(deadline)

        return date_format(deadline, "d.m.Y H:i")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображать имя категории в списке админки."""

    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)