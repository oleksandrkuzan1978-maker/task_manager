"""Представления создания, списка, просмотра, изменения и удаления подзадач задачи."""
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.task.models import Task, SubTask
from apps.serializers.subtasks import SubTaskCreateSerializer, SubTaskSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from apps.permissions import IsOwnerOrReadOnly

class SubTaskListCreateAPIView(ListCreateAPIView):
    """Получение списка подзадач и создание подзадач указанной задачи."""
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    queryset = SubTask.objects.select_related("task")

    # Фильтрация по полям
    filterset_fields = {"status": ["exact"],
                        "deadline": ["exact", "date"],}
    # Поиск по полям
    search_fields = ["title", "description"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return super().get_queryset().filter(task_id=self.kwargs["id"]
                                             , task__owner=self.request.user)

    # def get_queryset(self):
    #     task_ = get_object_or_404(Task, pk=self.kwargs["id"])
    #     return super().get_queryset().filter(task=task_)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SubTaskCreateSerializer
        return SubTaskSerializer

    def perform_create(self, serializer):
        task_ = get_object_or_404(Task, pk=self.kwargs["id"]
                                  , owner=self.request.user,)
        serializer.save(task=task_
                        , owner=self.request.user,)


class SubTaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Просмотр, обновление и удаление подзадачи указанной задачи."""
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    queryset = SubTask.objects.select_related("task")

    lookup_url_kwarg = "sub_id"

    def get_queryset(self):
        return super().get_queryset().filter(task_id=self.kwargs["id"]
                                             , task__owner=self.request.user,)

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Вернуть подзадачи от новых к старым, по пять на странице."""
        title = request.query_params.get("title", "").strip()
        status_ = request.query_params.get("status", "").strip()

        subtasks = SubTask.objects.filter(
                                        owner=request.user,
                                        task__owner=request.user,
                                    ).select_related("task")
        if title:
            subtasks = subtasks.filter(task__title__icontains=title)
        if status_:
            subtasks = subtasks.filter(status__icontains=status_)

        subtasks = subtasks.order_by("-created_at", "-id")

        return paginator(subtasks, request, "Subtasks")

