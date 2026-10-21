"""Модели проектов, задач, подзадач, категорий и тегов и варианты статуса."""

from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from  django.db.models.functions import TruncDate
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Status(models.TextChoices):
    """Строковые значения статуса задач и подзадач с переводимыми подписями."""

    NEW = "new", _("New")
    IN_PROGRESS = "in_progress", _("In progress")
    PENDING = "pending", _("Pending")
    BLOCKED = "blocked", _("Blocked")
    DONE = "done", _("Done")

class Project(models.Model):
    """Проект с уникальным названием, описанием и автоматически заданным временем создания."""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Project name"))
    description = models.TextField(verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    class Meta:
        """Метаданные и ограничения модели Project."""
        db_table = "project_manager_project"
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        constraints = [models.UniqueConstraint(fields=["name",], name="unique_project_name")]


class Task(models.Model):
    """Задача с категориями, тегами, статусом и необязательным сроком выполнения.
    Уникальность названия за дату создания проверяется моделью и ограничением базы данных."""

    title = models.CharField(max_length=80
                             , unique_for_date='created_at'
                             , verbose_name=_("Title")
                             , validators=[])
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    categories = models.ManyToManyField("Category", verbose_name=_("categories"), related_name="tasks")
    tags = models.ManyToManyField("Tag", verbose_name=_("Tags"), related_name="tasks")
    status = models.CharField(choices=Status, default=Status.NEW, max_length=20, verbose_name=_("Status"))
    deadline = models.DateTimeField(blank=True, null=True, verbose_name=_("Deadline"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    # {
    #     "title": "Подготовить отчёт",
    #     "description": "Собрать данные и подготовить итоговый отчёт",
    #     "categories": [1, 2],
    #     "tags": [1, 3],
    #     "deadline": "2026-10-20T18:00:00+02:00"
    # }

    class Meta:
        """Метаданные и ограничения модели Task."""
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
    """Подзадача со статусом и необязательным сроком, связанная с одной задачей.
    Удаляется каскадно при удалении родительской задачи."""

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
        """Метаданные и ограничения модели SubTask."""
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
    """Категория задач с уникальным именем и значением Other по умолчанию."""

    name = models.CharField(max_length=80, default="Other", unique=True, verbose_name=_("Category"))

    class Meta:
        """Метаданные и ограничения модели Category."""
        db_table = "task_manager_category"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_category"),]

    def __str__(self):
        """Вернуть имя категории."""

        return self.name

class Tag(models.Model):
    """Тег с уникальным именем для связи с задачами."""
    name = models.CharField(max_length=80, unique=True, verbose_name=_("Tag"))

    class Meta:
        """Метаданные и ограничения модели Tag."""
        db_table = "task_manager_tag"
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        constraints = [models.UniqueConstraint(fields=["name"], name="unique_tag"),]


