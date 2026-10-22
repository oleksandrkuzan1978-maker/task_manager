"""Представления создания и частичного обновления категорий."""
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.task.models import Category
from apps.serializers.categories import CategoryCreateSerializer

class CategoryGetAllCreateAPIView(APIView):
    """Метод создания категории past, не подключённый к HTTP POST; обработчик GET отсутствует."""
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
    def patch(self, request, id):
        """Найти категорию, проверить входные данные и сохранить частичное обновление."""
        category = get_object_or_404(Category, id=id)
        serializer = CategoryCreateSerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)