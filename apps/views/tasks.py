"""Представления списка задач, отдельной задачи и сводной статистики."""
from django.db import OperationalError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from apps.permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.task.models import Task, Status
from apps.serializers.tasks import (TaskCreateSerializer, TaskSerializer, TaskDetailSerializer)

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter, OrderingFilter
from apps.permissions import OnlyAdmin


class TaskListCreateAPIView(ListCreateAPIView):
    """Получение списка задач и создание новой задачи."""
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    queryset = Task.objects.prefetch_related("categories", "tags")
    #serializer_class = TaskCreateSerializer
    # Получаем фильтрацию, поиск и сортировку.
    #filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Фильтрация по полям; status - точное совпадение; deadline - точное время или календарная дата.
    filterset_fields = {"status": ["exact"],
                        "deadline": ["exact", "date"],}
    # Поиск по полям
    search_fields = ["title", "description"]

    # Поля, по которым клиенту разрешено сортировать задачи.
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    # Раньше queryset содержал все задачи, теперь ограничиваю выборку задачами текущего пользователя.
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer


class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление отдельной задачи."""
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    queryset = Task.objects.prefetch_related("categories", "tags", "subtasks",)

    #В существующем маршруте используется <int:id>
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user
        )

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return TaskCreateSerializer
        return TaskDetailSerializer


class TaskDetailAPIView(APIView):
    """Получение отдельной задачи со связанными подзадачами."""
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, id):
        """Представление для получения конкретной задачи."""
        task = get_object_or_404(
            Task,
            id=id,
            owner=request.user)

        self.check_object_permissions(request, task)

        serializer = TaskDetailSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskAggregateAPIView(APIView):
    """Получение общего количества задач, распределения по статусам и числа просроченных задач."""
    permission_classes = [IsAuthenticated, OnlyAdmin]

    def get(self, request):
        """Посчитать задачи и просроченные задачи без DONE; обработать доступные в try ошибки OperationalError."""
        try:
            #получение общего количества задач
            total_count_tasks = Task.objects.filter(
                                                    owner=request.user
                                                ).aggregate(total_count_of_tasks=Count('id'))

            #получение количества задач по каждому статусу
            count_tasks_of_status = list(Task.objects.filter(
                                                            owner=request.user
                                                        ).values('status').annotate(count_tasks_of_status=Count('id')))

            #получение количества просроченных задач
            # count_overdue_tasks = Task.objects.filter((~Q(status=Status.DONE) | Q(deadline=None))
            #                                           & Q(deadline__lt=timezone.now())
            #                                           ).aggregate(count_overdue_tasks=Count('id'))

            count_overdue_tasks = (Task.objects.filter(deadline__lt=timezone.now()
                                                       , owner=request.user).exclude(status=Status.DONE)
                                   .aggregate(count_overdue_tasks=Count('id')))
        except OperationalError:
            return Response({"error": "Unable to retrieve statistics. Please try again later."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response([total_count_tasks,
                         count_tasks_of_status,
                         count_overdue_tasks],
                        status=status.HTTP_200_OK)

