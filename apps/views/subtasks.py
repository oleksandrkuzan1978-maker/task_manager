"""Представления создания, списка, просмотра, изменения и удаления подзадач задачи."""

from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.task.models import Task, SubTask
from apps.serializers.subtasks import SubTaskCreateSerializer, SubTaskSerializer


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
        """Вернуть подзадачи от новых к старым, не более пяти на странице."""
        # def paginator(subtasks):
        #     if subtasks.exists():
        #         paginator = PageNumberPagination() # создаем пагинатор
        #         paginator.page_size = 5 # задаем размер страницы (пять подзадач на странице)
        #
        #         page = paginator.paginate_queryset(subtasks, request) #получаем только нужную страницу
        #                                                               # (номер страницы берется из параметра page в URL)
        #         serializer = SubTaskSerializer(page, many=True)
        #
        #         return paginator.get_paginated_response(serializer.data)
        #     else:
        #         return Response({"SubTasks": "SubTasks not found"}, status=status.HTTP_404_NOT_FOUND)

        task = get_object_or_404(Task, pk=id)

        title = request.query_params.get('title', "").strip()
        status = request.query_params.get('status', "").strip()

        #Если параметров нет
        if title is None and status is None:

            subtasks = task.subtasks.order_by("-created_at", "-id")

            return paginator(subtasks, request, "SubTasks")

        elif title and status:
            task_by_title = get_object_or_404(Task, title__icontains=title)

            subtasks_by_status = (task_by_title.subtasks
                                  .filter(status__icontains=status)
                                  .order_by("-created_at", "-id"))
            return paginator(subtasks_by_status, request, "Subtasks")

        elif title:
            task_by_title = get_object_or_404(Task, title__icontains=title)

            return paginator(task_by_title.subtasks.order_by("-created_at", "-id")
                             , request, "SubTasks")

        elif status:
            subtasks_by_status = (task.subtasks
                                  .filter(status__icontains=status)
                                  .order_by("-created_at", "-id"))
            return paginator(subtasks_by_status, request, "Subtasks")




# "Тест a3cd1b3214a74480ba9372c901c46857: Житель вперед выкинуть."
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
