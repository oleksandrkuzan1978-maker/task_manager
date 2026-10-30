from django.utils import timezone
from rest_framework import serializers
from apps.task.models import Task
from .subtasks import SubTaskSerializer

class TaskSerializer(serializers.ModelSerializer):

    """Сериализатор задачи без описания; идентификатор и время создания доступны только для чтения."""
    class Meta:
        """Поля и параметры сериализации TaskSerializer."""
        model = Task
        exclude = ('description',)
        read_only_fields = ('id', 'created_at',)


class TaskCreateSerializer(serializers.ModelSerializer):

    """Сериализатор всех полей задачи с проверкой срока выполнения."""
    class Meta:
        """Поля и параметры сериализации TaskCreateSerializer."""
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)

    @staticmethod
    def validate_deadline(value):
        """Отклонить срок в прошлом; разрешить отсутствие срока."""
        if value is not None and value < timezone.now():
            raise serializers.ValidationError("deadline must be greater than now")
        return value

class TaskDetailSerializer(serializers.ModelSerializer):

    """Сериализатор всех полей задачи с полными данными связанных подзадач только для чтения."""
    subtasks = SubTaskSerializer(many=True, read_only=True)
    class Meta:
        """Поля и параметры сериализации TaskDetailSerializer."""
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'created_at')
