
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.task.models import Task
from apps.task.serializers import SubTaskCreateSerializer


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
