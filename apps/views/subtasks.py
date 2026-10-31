"""Представления создания, списка, просмотра, изменения и удаления подзадач задачи."""

from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.task.models import Task, SubTask
from apps.serializers.subtasks import SubTaskCreateSerializer, SubTaskSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from orm_requests import task


class SubTaskListCreateAPIView(ListCreateAPIView):
    """Получение списка подзадач и создание подзадач указанной задачи."""
    queryset = SubTask.objects.select_related("task")

    # Фильтрация по полям
    filterset_fields = {"status": ["exact"],
                        "deadline": ["exact", "date"],}
    # Поиск по полям
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return super().get_queryset().filter(task_id=self.kwargs["id"],)

    # def get_queryset(self):
    #     task_ = get_object_or_404(Task, pk=self.kwargs["id"])
    #     return super().get_queryset().filter(task=task_)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SubTaskCreateSerializer
        return SubTaskSerializer

    def perform_create(self, serializer):
        task_ = get_object_or_404(Task, pk=self.kwargs["id"])
        serializer.save(task=task_)


class SubTaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Просмотр, обновление и удаление подзадачи указанной задачи."""
    queryset = SubTask.objects.select_related("task")

    lookup_url_kwarg = "sub_id"

    def get_queryset(self):
        return super().get_queryset().filter(task_id=self.kwargs["id"],)

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return SubTaskCreateSerializer
        return SubTaskSerializer









def paginator(pages, request, name_pages):
    if pages.exists():
        paginator = PageNumberPagination()  # создаем пагинатор

        paginator.page_size = 5  # задаем размер страницы (пять подзадач на странице)

        page = paginator.paginate_queryset(pages, request)  # получаем только нужную страницу

        # (номер страницы берется из параметра page в URL)
        serializer = SubTaskSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
    else:
        return Response({f"{name_pages}": f"{name_pages} not found"}, status=status.HTTP_404_NOT_FOUND)
        #return Response({"Error": "Objects not found"}, status=status.HTTP_404_NOT_FOUND)

class SubtaskGetByParamAPIView(APIView):
    """Список подзадач с фильтрами по названию задачи и статусу."""
    def get(self, request):
        """Вернуть подзадачи от новых к старым, по пять на странице."""
        title = request.query_params.get("title", "").strip()
        status_ = request.query_params.get("status", "").strip()

        subtasks = SubTask.objects.select_related("task")

        if title:
            subtasks = subtasks.filter(task__title__icontains=title)
        if status_:
            subtasks = subtasks.filter(status__icontains=status_)

        subtasks = subtasks.order_by("-created_at", "-id")

        return paginator(subtasks, request, "Subtasks")


# "Тест a3cd1b3214a74480ba9372c901c46857: Житель вперед выкинуть."

class SubTaskGetAllCreateAPIView(APIView):
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
        serializer = SubTaskSerializer(subtask)
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id, sub_id):
        """Удалить подзадачу указанной задачи и вернуть ответ 204 без тела."""
        task = get_object_or_404(Task, id=id)
        subtask = get_object_or_404(task.subtasks, id=sub_id)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
