"""Общий интерфейс импорта представлений задач, категорий, подзадач и главной страницы."""
from .tasks import (
    TaskGetAllCreateAPIView,
    TaskDetailAPIView,
    TaskAggregateAPIView,
    TaskListCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
)
from .subtasks import  (
    SubTaskGetAllCreateAPIView,
    SubTaskDetailUpdateDeleteView,
    SubtaskGetByParamAPIView,
    SubTaskListCreateAPIView,
    SubTaskRetrieveUpdateDestroyAPIView,
)
from .categories import (
    CategoryDetailAPIView,
    CategoryGetAllCreateAPIView,
)

from .index import index
from .variables import *