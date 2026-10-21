"""Общий интерфейс импорта представлений задач, категорий, подзадач и главной страницы."""
from .tasks import (
    TaskGetAllCreateAPIView,
    TaskDetailAPIView,
    TaskAggregateAPIView,
)
from .subtasks import  (
    SubTaskListCreateAPIView,
    SubTaskDetailUpdateDeleteView,
)
from .categories import (
    CategoryDetailAPIView,
    CategoryGetAllCreateAPIView,
)

from .index import index