"""Административный интерфейс задач, подзадач, категорий и тегов."""
from itertools import count

from django.contrib import admin
from .models import Task, SubTask, Category, Status, Tag
from django.utils import timezone
from django.contrib import messages
from django.utils.formats import date_format


# Register your models here.

#admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)

class SubTaskInline(admin.TabularInline):
    """Редактирование подзадач в табличном блоке формы родительской задачи."""
    model = SubTask
    fields = ('title', 'status', 'description', 'deadline')
    show_change_link = True
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Настройки списка, поиска и редактирования задач с категориями, тегами и подзадачами."""

    list_display = ('short_title', 'status', 'created_at', 'deadline')
    search_fields = ('title',)
    ordering = ('-created_at',)
    fields = ('title', 'status','categories', 'tags', 'description', 'deadline')
    list_per_page = 10

    inlines = [SubTaskInline]

    @admin.display(description="Название", ordering="title")
    def short_title(self, obj):
        """Вернуть название, сократив его до 10 символов с многоточием при превышении длины."""
        return obj.title[:10] + "..." if len(obj.title) > 10 else obj.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    """Настройки списка, поиска и редактирования подзадач и массовой смены статуса."""

    list_display = ('title', 'task', 'status', 'created_at', 'deadline')
    search_fields = ('title', 'task__title')
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
    list_display = ('name', "is_deleted", "deleted_at")
    list_filter = ('is_deleted',)
    search_fields = ('name',)
    fields = ('name',)

    # Признаки удаления отображаем, но не редактируем вручную.
    fields = ('name', "is_deleted", "deleted_at")
    readonly_fields = ("is_deleted", "deleted_at")

    actions = (
        "soft_delete_selected",
        "restore_selected",
        "hard_delete_selected",
    )

    def get_queryset(self, request):
        """В админке показываем активные и удалённые категории."""
        return Category.all_objects.all().order_by('name')

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Убираем стандартное массовое действие с неоднозначной подписью.
        actions.pop("delete_selected", None)
        return actions

    @admin.action( description="Мягко удалить выбранные категории",
                   permissions=["delete"],)
    def soft_delete_selected(self, request, queryset):
        count_ = queryset.soft_delete()

        self.message_user(request, f"Мягко удалено категорий: {count_}.",
            messages.SUCCESS,)

    @admin.action(description="Восстановить выбранные категории",
        permissions=["change"],)
    def restore_selected(self, request, queryset):
        count_ = queryset.restore()

        self.message_user(request, f"Восстановлено категорий: {count}.",
            messages.SUCCESS,)

    @admin.action(description="Удалить из БД выбранные удалённые категории",
        permissions=["delete"],)
    def hard_delete_selected(self, request, queryset):
        """hard_delete() удаляет только записи с is_deleted=True."""
        deleted = queryset.deleted()
        count_ = queryset.count()
        deleted.hard_delete()

        self.message_user(request,  f"Физически удалено категорий: {count}.",
            messages.SUCCESS,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Настройки списка, поиска и редактирования тегов в админке."""
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)
