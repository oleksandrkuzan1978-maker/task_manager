from django.db import OperationalError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.task.models import Category
from apps.task.serializers import CategoryCreateSerializer

class CategoryGetAllCreateAPIView(APIView):
    def past(self, request):
        """представление для создания новой категории."""
        serializer = CategoryCreateSerializer(data=request.data)
        print(request, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    def patch(self, request, id):
        category = get_object_or_404(Category, id=id)
        serializer = CategoryCreateSerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)