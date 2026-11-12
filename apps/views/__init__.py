"""Общий интерфейс импорта представлений задач, категорий, подзадач и главной страницы."""
from .tasks import (
    TaskDetailAPIView,
    TaskAggregateAPIView,
    TaskListCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
)
from .subtasks import  (
    SubtaskGetByParamAPIView,
    SubTaskListCreateAPIView,
    SubTaskRetrieveUpdateDestroyAPIView,
)
from .categories import (
    CategoryDetailAPIView,
    CategoryGetAllCreateAPIView,
    CategoryViewSet,
)

from .index import index
from .variables import *