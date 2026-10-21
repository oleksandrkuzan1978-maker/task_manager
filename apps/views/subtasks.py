"""Представления создания, списка, просмотра, изменения и удаления подзадач задачи."""

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.task.models import Task
from apps.task.serializers import SubTaskCreateSerializer

class SubTaskListCreateAPIView(APIView):
    """Создание подзадачи и получение списка подзадач указанной задачи."""
    def post(self, request, id):
        """Проверить входные данные и сохранить подзадачу для задачи из URL."""

        task = get_object_or_404(Task, id=id)

        serializer = SubTaskCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        """Вернуть подзадачи по идентификатору или ответ 404, если список пуст."""
        task = get_object_or_404(Task, id=id)

        subtasks = task.subtasks.order_by("id")
        if subtasks.exists():
            serializer = SubTaskCreateSerializer(subtasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"SubTasks": "SubTasks not found"}, status=status.HTTP_404_NOT_FOUND)


class SubTaskDetailUpdateDeleteView(APIView):
    """Просмотр, частичное обновление и удаление подзадачи указанной задачи."""
        
    def get(self, request, id, sub_id):
        """Вернуть подзадачу, проверив её принадлежность указанной задаче."""
        task=get_object_or_404(Task, id=id)
        subtask=get_object_or_404(task.subtasks, id=sub_id)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    def patch(self, request, id, sub_id):
        """Проверить и частично обновить подзадачу указанной задачи."""
        task = get_object_or_404(Task, id=id)
        subtask = get_object_or_404(task.subtasks, id=sub_id)
        serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, id, sub_id):
        """Удалить подзадачу указанной задачи и вернуть ответ 204 без тела."""
        task = get_object_or_404(Task, id=id)
        subtask = get_object_or_404(task.subtasks, id=sub_id)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
