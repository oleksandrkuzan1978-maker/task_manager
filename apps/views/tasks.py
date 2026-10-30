"""Представления списка задач, отдельной задачи и сводной статистики."""
from django.db import OperationalError
from django.utils import timezone
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.task.models import Task, Status
from apps.serializers.tasks import (TaskCreateSerializer, TaskSerializer, TaskDetailSerializer)

from .variables import weekdays, message_response_weekday

from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter, OrderingFilter

class TaskListCreateAPIView(ListCreateAPIView):
    """Получение списка задач и создание новой задачи."""
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

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer


class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление отдельной задачи."""
    queryset = Task.objects.prefetch_related("categories", "tags", "subtasks",)
    #serializer_class = TaskSerializer

    #В существующем маршруте используется <int:id>
    lookup_url_kwarg = "id"

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return TaskCreateSerializer
        return TaskDetailSerializer








class TaskGetAllCreateAPIView(APIView):
    """Список задач и метод создания past, не подключённый к HTTP POST."""
    def post(self, request):
        """Проверить входные данные и создать задачу; имя past не является обработчиком POST."""
        serializer = TaskCreateSerializer(data=request.data)
        print(request, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Вернуть задачи по идентификатору, или ответ 404, если список пуст.
        Предусмотрена возможность вывода списка задач по дню недели,
        в который были созданы задачи.
        Название дня недели вводится как параметр запроса."""
        weekday = request.query_params.get('weekday').strip().lower()
        if weekday:
            if weekday not in weekdays:
                return Response({"weekday": message_response_weekday},
                                status=status.HTTP_400_BAD_REQUEST, )
            tasks_by_weekday = (Task.objects.prefetch_related("categories", 'tags')
                                .filter(created_at__week_day=weekdays[weekday])
                                .order_by("id"))
            if tasks_by_weekday.exists():
                serializer = TaskSerializer(tasks_by_weekday, many=True)
                return Response({"Task creation day":weekday
                                    , "tasks":serializer.data}
                                , status=status.HTTP_200_OK)
            return Response({f"Tasks by {weekday}": "Tasks not found"}
                            , status=status.HTTP_404_NOT_FOUND)
        else:
            all_tasks = Task.objects.all().prefetch_related("categories", 'tags').order_by("id")
            if all_tasks.exists():
                serializer = TaskSerializer(all_tasks, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND)


class TaskDetailAPIView(APIView):
    """Получение отдельной задачи со связанными подзадачами."""
    def get(self, request, id):
        """Представление для получения конкретной задачи."""
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskAggregateAPIView(APIView):

    """Получение общего количества задач, распределения по статусам и числа просроченных задач."""
    def get(self, request):
        """Посчитать задачи и просроченные задачи без DONE; обработать доступные в try ошибки OperationalError."""
        try:
            #получение общего количества задач
            total_count_tasks = Task.objects.aggregate(total_count_of_tasks=Count('id'))

            #получение количества задач по каждому статусу
            count_tasks_of_status = list(Task.objects.values('status').annotate(count_tasks_of_status=Count('id')))

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

