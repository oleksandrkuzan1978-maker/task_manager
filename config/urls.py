"""Маршруты главной страницы, админки и API задач, статистики, категорий и подзадач."""
from django.contrib import admin
from django.urls import path
from apps import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('tasks/',views.TaskListCreateAPIView.as_view(), name="task_get_all_create"),
    path('tasks/<int:id>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name="task_detail"),
    path('tasks/aggregate/', views.TaskAggregateAPIView.as_view(), name="task_aggregate"),
    path('category/', views.CategoryGetAllCreateAPIView.as_view(), name="category_get_all_create"),
    path('category/<int:id>/', views.CategoryDetailAPIView.as_view(), name="category_detail"),
    path('task/<int:id>/subtasks/', views.SubTaskListCreateAPIView.as_view(), name="subtask_list_create"),
    path('task/<int:id>/subtasks/<int:sub_id>/', views.SubTaskRetrieveUpdateDestroyAPIView.as_view()
         , name="subtask_detail_update_delete"),
    path('subtasks/', views.SubtaskGetByParamAPIView.as_view(), name="subtask_get_by_param"),
]


