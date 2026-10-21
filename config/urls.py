"""Корневые маршруты проекта.

Список urlpatterns подключает административный интерфейс по пути admin/.
"""
from django.contrib import admin
from django.urls import path
from apps.task import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('tasks/',views.TaskGetAllCreateAPIView.as_view(), name="task_get_all_create"),
    path('tasks/<int:id>/', views.TaskDetailAPIView.as_view(), name="task_detail"),
    path('tasks/aggregate/', views.TaskAggregateAPIView.as_view(), name="task_aggregate"),
    path('category/', views.CategoryGetAllCreateAPIView.as_view(), name="category_get_all_create"),
    path('category/<int:id>/', views.CategoryDetailAPIView.as_view(), name="category_detail"),
    path('task/<int:id>/subtasks/', views.SubTaskListCreateAPIView.as_view(), name="subtask_list_create"),
    path('task/<int:id>/subtasks/<int:sub_id>/', views.SubTaskDetailUpdateDeleteView.as_view()
         , name="subtask_detail_update_delete"),
]


