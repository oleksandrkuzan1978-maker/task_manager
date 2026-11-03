from itertools import count

from django.db import models
from django.utils import timezone

class DeleteQuerySet(models.QuerySet):
    def active(self):
        """Только неудалённые записи."""
        return self.filter(is_deleted=False)

    def soft_delete(self):
        """Мягкое удаление нескольких записей."""
        return self.active().update(is_deleted=True
                           , deleted_at=timezone.now())

    def delete(self):
        """Обычное массовое удаление тоже должно быть мягким."""
        deleted_count = self.soft_delete()
        return deleted_count, {"number of soft-deleted records": deleted_count}

    def full_delete(self):
        """Физическое удаление из БД любой записи без разбору"""
        return super().delete()


class SoftDeleteQuerySet(DeleteQuerySet):
    def deleted(self):
        """Только мягко удалённые записи."""
        return self.filter(is_deleted=True)

    def restore(self):
        """Восстановление сразу нескольких записей."""
        return self.deleted().update(is_deleted=False
                           , deleted_at=None)

    def hard_delete(self):
        """Физическое удаление только мягко удаленных записей"""
        return self.deleted().full_delete()


class SoftDeleteManager(models.Manager.from_queryset(DeleteQuerySet)):
    def get_queryset(self):
        return super().get_queryset().active()

class TaskManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(categories__is_deleted=False).distinct()

