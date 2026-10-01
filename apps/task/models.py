"""Модели задач, подзадач и категорий и общие варианты статуса."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from  django.db.models.functions import TruncDate

# Create your models here.

class Status(models.TextChoices):
    """Строковые значения статуса задач и подзадач с переводимыми подписями."""

    NEW = "new", _("New")
    IN_PROGRESS = "in_progress", _("In progress")
    PENDING = "pending", _("Pending")
    BLOCKED = "blocked", _("Blocked")
    DONE = "done", _("Done")


class Task(models.Model):
    """Задача с категориями, статусом и необязательным сроком выполнения.

    Проверка модели требует уникальности названия в пределах даты
    created_at через unique_for_date; это не ограничение базы данных.
    Описание может быть пустым, срок — отсутствовать. Время создания
    заполняется автоматически при первом сохранении.

    Attributes:
        title: Название длиной до 80 символов.
        description: Текстовое описание задачи.
        categories: Связь многие-ко-многим с категориями.
        status: Значение Status; по умолчанию NEW.
        deadline: Срок выполнения или None.
        created_at: Дата и время создания записи.
    """

    title = models.CharField(max_length=80, unique_for_date='created_at', verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    categories = models.ManyToManyField("Category", verbose_name=_("categories"), related_name="tasks")
    status = models.CharField(choices=Status, default=Status.NEW, max_length=20, verbose_name=_("Status"))
    deadline = models.DateTimeField(blank=True, null=True, verbose_name=_("Deadline"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        db_table = "task_manager_task"
        ordering = ["-created_at"]
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        constraints = [
            models.UniqueConstraint(
                TruncDate("created_at"),
                "title",
                name="unique_task_title_per_created_date",
            ),
        ]

    def __str__(self):
        """Вернуть название"""

        return self.title


class SubTask(models.Model):
    """Подзадача, принадлежащая одной задаче.

    Удаляется каскадно при удалении родительской задачи. Доступна
    через обратную связь Task.subtasks. Описание может быть пустым,
    а срок выполнения — отсутствовать.

    Attributes:
        title: Название длиной до 80 символов.
        description: Текстовое описание подзадачи.
        task: Родительская задача.
        status: Значение Status; по умолчанию NEW.
        deadline: Срок выполнения или None.
        created_at: Время создания, заполняемое при первом сохранении.
    """

    title = models.CharField(max_length=80, verbose_name=_("SubTask"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
        verbose_name=_("Task"),
    )
    status = models.CharField(choices=Status, default=Status.NEW, max_length=20, verbose_name=_("Status"))
    deadline = models.DateTimeField(blank=True, null=True, verbose_name=_("Deadline"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        db_table = "task_manager_subtask"
        ordering = ["-created_at"]
        verbose_name = _("Subtask")
        verbose_name_plural = _("Subtasks")
        constraints = [models.UniqueConstraint(
                fields=["title", "task"],
                name="unique_subtask_title_per_task",
            ),]

    def __str__(self):
        """Вернуть название подзадачи."""

        return self.title


class Category(models.Model):
    """Категория для группировки задач.

    Attributes:
        name: Имя длиной до 80 символов; по умолчанию Other.
    """

    name = models.CharField(max_length=80, default="Other", unique=True, verbose_name=_("Category"))

    class Meta:
        db_table = "task_manager_category"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_category"),]

    def __str__(self):
        """Вернуть имя категории."""

        return self.name

