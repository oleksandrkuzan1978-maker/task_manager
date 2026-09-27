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

    title = models.CharField(max_length=80, unique_for_date='created_at')
    description = models.TextField(blank=True)
    categories = models.ManyToManyField("Category", verbose_name="Categories")
    status = models.CharField(choices=Status, default=Status.NEW, max_length=20)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                TruncDate("created_at"),
                "title",
                name="unique_task_title_per_created_date",
            ),
        ]

    def __str__(self):
        """Вернуть название, срок выполнения и время создания задачи.

        Returns:
            str: Значения полей, разделенные запятой и пробелом.
        """

        return f"{self.title}, {self.deadline}, {self. created_at}"


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

    title = models.CharField(max_length=80, verbose_name="SubTask")
    description = models.TextField(blank=True)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
    )
    status = models.CharField(choices=Status, default=Status.NEW, max_length=20)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Вернуть название, срок выполнения и время создания подзадачи.

        Returns:
            str: Значения полей, разделенные запятой и пробелом.
        """

        return f"{self.title}, {self.deadline}, {self. created_at}"


class Category(models.Model):
    """Категория для группировки задач.

    Attributes:
        name: Имя длиной до 80 символов; по умолчанию Other.
    """

    name = models.CharField(max_length=80, default="Other")

    def __str__(self):
        """Вернуть имя категории.

        Returns:
            str: Значение поля name.
        """

        return self.name