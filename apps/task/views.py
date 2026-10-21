"""Модуль представлений приложения задач.

Представления пока не реализованы.
"""
from django.db import OperationalError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse


from .models import Task, Status, Category, SubTask
from .serializers import (TaskSerializer, CategoryCreateSerializer,
                          TaskDetailSerializer, SubTaskCreateSerializer)


# Create your views here.

def index(request):
    return HttpResponse("Главная страница")


class TaskGetAllCreateAPIView(APIView):

    def past(self, request):
        """представление для создания новой задачи."""
        serializer = TaskSerializer(data=request.data)
        print(request, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """ Представление для получения списка задач"""
        tasks = Task.objects.all().order_by("id")
        if tasks.exists():
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND)


class TaskDetailAPIView(APIView):

    def get(self, request, id):
        """Представление для получения конкретной задачи."""
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskAggregateAPIView(APIView):

    def get(self, request):
        """ Представление для получения общего количества задач, количества задач по каждому статусу
        и количества просроченных задач."""
        try:
            #получение общего количества задач
            total_count_tasks = Task.objects.aggregate(total_count_of_tasks=Count('id'))

            #получение количества задач по каждому статусу
            count_tasks_of_status = Task.objects.values('status').annotate(count_tasks_of_status=Count('id'))

            #получение количества просроченных задач
            # count_overdue_tasks = Task.objects.filter((~Q(status=Status.DONE) | Q(deadline=None))
            #                                           & Q(deadline__lt=timezone.now())
            #                                           ).aggregate(count_overdue_tasks=Count('id'))

            count_overdue_tasks = (Task.objects.filter(deadline__lt=timezone.now()).exclude(status=Status.DONE)
                                   .aggregate(count_overdue_tasks=Count('id')))
        except OperationalError:
            return Response({"error": "Unable to retrieve statistics. Please try again later."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response([total_count_tasks,
                         count_tasks_of_status,
                         count_overdue_tasks],
                        status=status.HTTP_200_OK)


class CategoryGetAllCreateAPIView(APIView):

    def past(self, request):
        """представление для создания новой категории."""
        serializer = CategoryCreateSerializer(data=request.data)
        print(request, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailAPIView(APIView):

    def patch(self, request, id):
        category = get_object_or_404(Category, id=id)
        serializer = CategoryCreateSerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


# Задание 5: Создание классов представлений
# Создайте классы представлений для работы с подзадачами (SubTasks),
# включая создание, получение, обновление и удаление подзадач.
# Используйте классы представлений (APIView) для реализации этого функционала.
# Шаги для выполнения:
# Создайте классы представлений для создания
# и получения списка подзадач (SubTaskListCreateView).
# Создайте классы представлений для получения, обновления
# и удаления подзадач (SubTaskDetailUpdateDeleteView).
# Добавьте маршруты в файле urls.py, чтобы использовать эти классы.

class SubTaskListCreateAPIView(APIView):
    def post(self, request, id):
        """представление для создания новой подзадачи."""

        task = get_object_or_404(Task, id=id)

        serializer = SubTaskCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        task = get_object_or_404(Task, id=id)

        subtasks = task.subtasks.order_by("id")
        if subtasks.exists():
            serializer = SubTaskCreateSerializer(subtasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"SubTasks": "SubTasks not found"}, status=status.HTTP_404_NOT_FOUND)

class SubTaskDetailUpdateDeleteView(APIView):

    def get(self, request, id, sub_id):
        task=get_object_or_404(Task, id=id)
        subtask=get_object_or_404(task.subtasks, id=sub_id)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    def patch(self, request, id, sub_id):
        task = get_object_or_404(Task, id=id)
        subtask = get_object_or_404(task.subtasks, id=sub_id)
        serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id, sub_id):
        task = get_object_or_404(Task, id=id)
        subtask = get_object_or_404(task.subtasks, id=sub_id)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
