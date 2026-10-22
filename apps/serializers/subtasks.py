from rest_framework import serializers
from apps.task.models import SubTask


class SubTaskCreateSerializer(serializers.ModelSerializer):
    """Сериализатор всех полей подзадачи с временем создания только для чтения."""
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        """Поля и параметры сериализации SubTaskCreateSerializer."""
        model = SubTask
        fields = '__all__'
        read_only_fields = ('id', 'created_at', "task")


class SubTaskSerializer(serializers.ModelSerializer):
    """Полное представление подзадачи."""

    class Meta:
        model = SubTask
        fields = "__all__"


