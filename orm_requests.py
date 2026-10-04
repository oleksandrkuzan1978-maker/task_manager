import os
from datetime import timedelta

from django.utils import timezone

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.task.models import Task, Category, Status, SubTask

#Task:
# title: "Prepare presentation".
# description: "Prepare materials and slides for the presentation".
# status: "New".
# deadline: Today's date + 3 days.
try:
    task = Task.objects.get(title="Prepare presentation")
    task.delete()
except Task.DoesNotExist:
    print(f'Создаем новую запись в таблице {Task._meta.db_table}:')

task = Task.objects.create(
    title='Prepare presentation',
    description='Prepare materials and slides for the presentation',
    status=Status.NEW,
    deadline=timezone.now() + timedelta(days=3),
)
cat = Category.objects.get(name='Работа')
task.categories.add(cat)
# проверяем внесение категории в запись задачи
category_names = ", ".join(
    category.name for category in task.categories.all()
)
t=4*'\t'
print(f"{t}Задача: {task.title}\n{t}Описание: {task.description}"
      f"\n{t}Срок сдачи: {task.deadline}\n{t}Статус: {task.status}\n{t}Категория: {category_names}")
#print(f"\nНапоминание: срок главной задачи — {task.deadline}\n")

# SubTasks для "Prepare presentation":
# title: "Gather information".
# description: "Find necessary information for the presentation".
# status: "New".
# deadline: Today's date + 2 days.
subtask1 = SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status=Status.NEW,
    deadline=timezone.now() + timedelta(days=2),
    task=task
)


# title: "Create slides".
# description: "Create presentation slides".
# status: "New".
# deadline: Today's date + 1 day.
subtask2 = SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status=Status.NEW,
    deadline=timezone.now() + timedelta(days=1),
    task=task
)

# Чтение записей:
# Tasks со статусом "New":
# Вывести все задачи, у которых статус "New".
# SubTasks с просроченным статусом "Done":
# Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.

status = Status.DONE
subtask_done = SubTask.objects.filter(status=status, deadline__lt=timezone.now())
print(f"Список подзадач задачи {task.title}, которые имеют статус {status}:")
for subtask in subtask_done:
    print(t, f"'{subtask.title}'")


# Изменение записей:
# Измените статус "Prepare presentation" на "In progress".
print("\nЗначение task.status до изменения:", task.status)
task.status = Status.IN_PROGRESS
task.save()
print("Значение task.status после изменения:", task.status)


# # Измените срок выполнения для "Gather information" на два дня назад.
print("\nЗначение subtask1.deadline до изменения:", subtask1.deadline)
subtask1.deadline = subtask1.deadline - timedelta(days=2)
subtask1.save()
print("Значение subtask1.deadline после изменения:", subtask1.deadline)


# # Измените описание для "Create slides" на "Create and format presentation slides".
print("\nЗначение subtask2.deadline до изменения:", subtask2.description)
subtask2.description = "Create and format presentation slides"
subtask2.save()
print("Значение subtask2.deadline после изменения:", subtask2.description)

# # Удаление записей:
# # Удалите задачу "Prepare presentation" и все ее подзадачи.

#task = Task.objects.get(title="Prepare presentation")
task.delete()

# проверка удаления задачи и всех ее подзадач
print("\nПроверка удаления задачи и всех ее подзадач")

has_subtasks = SubTask.objects.filter(
    task__title="Prepare presentation"
).exists()

if has_subtasks:
    print("У задачи остались неудаленные подзадачи")
else:
    task = Task.objects.filter(title="Prepare presentation")
    if not task:
        print(f'{task}: Задача и ее подзадачи удалены')
    else:
        print('Задача не удалена')

