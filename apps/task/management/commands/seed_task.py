"""Команда создания тестовых задач, подзадач и категорий с необязательной очисткой."""
import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from faker import Faker

from apps.task.models import (Task, SubTask, Category, Status)

faker = Faker('ru_RU')


class Command(BaseCommand):
    """Команда заполнения базы тестовыми задачами, подзадачами и категориями."""
    help = 'Заполняет базу тестовыми данными'

    def add_arguments(self, parser):
        """Добавить выбор владельца и флаг очистки данных."""
        parser.add_argument(
            '--owner', required=True,
            help='Имя существующего пользователя, которому принадлежат тестовые задачи.',
        )
        parser.add_argument('--clear', action='store_true'
                            , help='Удалить старые данные перед заполнением')

    @transaction.atomic # если что-то упадёт, в базу не запишется ничего
    def handle(self, *args, **options):
        """Создать тестовые задачи, категории и связанные подзадачи."""
        from uuid import uuid4

        user_model = get_user_model()
        username = options['owner']
        try:
            owner = user_model._default_manager.get_by_natural_key(username)
        except user_model.DoesNotExist:
            raise CommandError(f'Пользователь {username!r} не найден.') from None

        if options.get('clear', False):
            self.clear()

        categories = [
            Category.objects.get_or_create(name=name)[0]
            for name in ('Работа', 'Учёба', 'Дом', 'Личное', 'Other')
        ]
        now = timezone.now()
        task_count = 20
        subtask_count = 0

        for _ in range(task_count):
            # UUID позволяет повторять заполнение без совпадений названий за день.
            title = f'Тест {uuid4().hex}: {faker.sentence(nb_words=4)}'
            deadline = (
                now + timedelta(days=random.randint(1, 30))
                if random.choice((True, False)) else None
            )
            task = Task(
                owner=owner,
                title=title[:Task._meta.get_field('title').max_length],
                description=faker.paragraph(nb_sentences=3),
                status=random.choice(Status.values),
                deadline=deadline,
            )
            # save() сам не запускает валидацию полей и ограничений модели.
            task.full_clean()
            task.save()

            # ManyToMany можно заполнить только после получения первичного ключа.
            task.categories.set(random.sample(categories, k=random.randint(1, 3)))

            for number in range(1, random.randint(1, 4) + 1):
                title = f'Подзадача {number}: {faker.sentence(nb_words=4)}'
                subtask = SubTask(
                    task=task,
                    owner=task.owner,
                    # Номер обеспечивает уникальность названия внутри задачи.
                    title=title[:SubTask._meta.get_field('title').max_length],
                    description=faker.paragraph(nb_sentences=2),
                    status=(
                        Status.DONE if task.status == Status.DONE
                        else random.choice(Status.values)
                    ),
                    # Срок подзадачи не выходит за срок родительской задачи.
                    deadline=(
                        deadline - timedelta(hours=random.randint(0, 23))
                        if deadline is not None else None
                    ),
                )
                subtask.full_clean()
                subtask.save()
                subtask_count += 1

        # Сообщаем об успехе только после фиксации внешней транзакции.
        message = (
            f'Создано задач: {task_count}, подзадач: {subtask_count}. '
            f'Использовано категорий: {len(categories)}.'
        )
        transaction.on_commit(
            lambda: self.stdout.write(self.style.SUCCESS(message))
        )

    @transaction.atomic
    def clear(self):
        """Удалить все задачи, их подзадачи и категории из базы данных."""
        # Django каскадно удалит подзадачи и промежуточные связи ManyToMany.
        Task.objects.all().delete()
        Category.objects.all().delete()
