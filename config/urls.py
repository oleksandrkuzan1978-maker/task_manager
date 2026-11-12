"""Маршруты главной страницы, админки и API задач, статистики, категорий и подзадач."""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from apps import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="First API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@local.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    )

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename="category")

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('tasks/',views.TaskListCreateAPIView.as_view(), name="task_get_all_create"),
    path('tasks/<int:id>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name="task_detail"),
    path('tasks/aggregate/', views.TaskAggregateAPIView.as_view(), name="task_aggregate"),
    path('category/', views.CategoryGetAllCreateAPIView.as_view(), name="category_get_all_create"),
    path('category/<int:id>/', views.CategoryDetailAPIView.as_view(), name="category_detail"),

    path('', include(router.urls)),

    path('task/<int:id>/subtasks/', views.SubTaskListCreateAPIView.as_view(), name="subtask_list_create"),
    path('task/<int:id>/subtasks/<int:sub_id>/', views.SubTaskRetrieveUpdateDestroyAPIView.as_view()
         , name="subtask_detail_update_delete"),
    path('subtasks/', views.SubtaskGetByParamAPIView.as_view(), name="subtask_get_by_param"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')

]


