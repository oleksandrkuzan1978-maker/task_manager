"""Представления создания и частичного обновления категорий."""
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.task.models import Category
from apps.serializers.categories import CategoryCreateSerializer
from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.order_by("id")
    serializer_class = CategoryCreateSerializer
    #permission_classes = [IsAuthenticated, StaffOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        # Для восстановления и окончательного удаления
         #нужны все категории, включая мягко удалённые.
        if self.action in ("restore", "hard_delete"):
            return Category.all_objects.order_by("id")
        # Для остальных действий — только активные категории.
        return super().get_queryset()

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        """Восстановить мягко удалённую категорию."""
        category = self.get_object()

        if not category.is_deleted:
            return Response({"detail": "The category is already active."},
                status=status.HTTP_400_BAD_REQUEST,)
        category.restore()
        serializer = self.get_serializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["delete"],  url_path="hard-delete",)
    def hard_delete(self, request, pk=None):
        """Физически удалить ранее мягко удалённую категорию."""
        category = self.get_object()
        if not category.is_deleted:
            return Response({"detail": "First, perform a soft delete."}
                            , status=status.HTTP_400_BAD_REQUEST )
        category.full_delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path="count-tasks",)
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        return Response({"id": category.pk,
                         "name": category.name,
                         "tasks_count": category.tasks.count(),})

class CategoryGetAllCreateAPIView(APIView):
    """Метод создания категории past, не подключённый к HTTP POST; обработчик GET отсутствует."""
    #permission_classes = [IsAuthenticated, StaffOrReadOnly]

    def post(self, request):
        """Проверить имя и создать категорию; имя past не является обработчиком POST."""
        serializer = CategoryCreateSerializer(data=request.data)
        #print(request, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        categories = Category.objects.order_by("id")
        serializer = CategoryCreateSerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetailAPIView(APIView):
    """Частичное обновление имени существующей категории."""
    #permission_classes = [IsAuthenticated, StaffOrReadOnly]

    def patch(self, request, id):
        """Найти категорию, проверить входные данные и сохранить частичное обновление."""
        category = get_object_or_404(Category, id=id)
        serializer = CategoryCreateSerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)