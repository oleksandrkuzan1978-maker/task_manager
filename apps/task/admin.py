"""Регистрация моделей задач, подзадач и категорий в админке Django."""

from django.contrib import admin
from .models import Task, SubTask, Category, Status
from django.utils import timezone
from django.contrib import messages
from django.utils.formats import date_format


# Register your models here.

#admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)

class SubTaskInline(admin.TabularInline):
    model = SubTask
    fields = ('title', 'status', 'description', 'deadline')
    show_change_link = True
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Отображать название и время создания задачи в списке админки."""

    list_display = ('short_title', 'status', 'created_at', 'deadline')
    search_fields = ('title',)
    ordering = ('-created_at',)
    fields = ('title', 'status', 'description', 'deadline')
    list_per_page = 10

    inlines = [SubTaskInline]

    @admin.display(description="Название", ordering="title")
    def short_title(self, obj):
        """Вернуть название, сократив его до 10 символов с многоточием при превышении длины."""
        return obj.title[:10] + "..." if len(obj.title) > 10 else obj.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    """Отображать название и время создания подзадачи в списке админки."""

    list_display = ('title', 'task', 'status', 'created_at', 'deadline')
    search_fields = ('title', 'task__title')
    ordering = ('-created_at', 'task')
    fields = ('title', 'task', 'status', 'description', 'deadline')
    list_per_page = 10

    @admin.action(description='Change status of SubTusk to Done')
    def status_to_done(self, request, queryset):
        """Отметить выбранные подзадачи выполненными и сообщить число обновлённых записей."""
        res = queryset.update(status=Status.DONE) #deadline=timezone.now()
        self.message_user(request, f'Changed SubTask status to done = {res}', messages.SUCCESS)

    actions = [status_to_done]

    @admin.display(description="Срок родительской задачи")
    def task_deadline_reminder(self, obj):
        """Вернуть срок родительской задачи или пояснение, если задача либо срок не указаны."""
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