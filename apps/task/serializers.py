"""Сериализация задач, подзадач и категорий и проверка входных данных API."""
from django.utils import timezone
from rest_framework import serializers
from .models import Task, Category, SubTask


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


class SubTaskCreateSerializer(serializers.ModelSerializer):
    """Сериализатор всех полей подзадачи с временем создания только для чтения."""
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        """Поля и параметры сериализации SubTaskCreateSerializer."""
        model = SubTask
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)


class SubTaskSerializer(serializers.ModelSerializer):
    """Полное представление подзадачи."""

    class Meta:
        model = SubTask
        fields = "__all__"


class TaskDetailSerializer(serializers.ModelSerializer):

    """Сериализатор всех полей задачи с полными данными связанных подзадач только для чтения."""
    subtasks = SubTaskSerializer(many=True, read_only=True)
    class Meta:
        """Поля и параметры сериализации TaskDetailSerializer."""
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)


class CategoryCreateSerializer(serializers.ModelSerializer):
    """Сериализатор имени категории с проверками уникальности при создании и обновлении."""
    class Meta:
        """Поля и параметры сериализации CategoryCreateSerializer."""
        model = Category
        fields = ['name',]
        extra_kwargs = {"name": {"default": Category._meta.get_field("name").get_default,},} #{"default": "Other"}

    def create(self, validated_data):
        """Проверить наличие категории с очищенным именем и создать категорию из входных данных."""
        name = validated_data['name'].strip()
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError({'name': 'Category with this name already exists!'})
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Обновить имя категории, проверив уникальность среди остальных категорий."""
        name = validated_data.get("name", instance.name).strip()
        # category_in_table = Category.objects.filter(name=name)
        category_in_table = Category.objects.filter(name=name).exclude(
            pk=instance.pk
        )
        if category_in_table.exists():
            raise serializers.ValidationError({'name': 'Category with this name already exists!'})
        else:
            instance.name = name
            instance.save()
            return instance



