from os import name
from django.utils import timezone
from rest_framework import serializers
from .models import Task, Category, SubTask

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        exclude = ('description',)
        read_only_fields = ('id', 'created_at',)


class TaskCreateSerializer(serializers.ModelSerializer):
    # Задание 4: Валидация данных в сериализаторах
    # Создайте TaskCreateSerializer и добавьте валидацию для поля deadline,
    # чтобы дата не могла быть в прошлом. Если дата в прошлом,
    # возвращайте ошибку валидации.
    # Шаги для выполнения:
    # Определите TaskCreateSerializer в файле serializers.py.
    # Переопределите метод validate_deadline для проверки даты.
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)

    def validate_deadline(self, value):
        if value is not None and value < timezone.now():
            raise serializers.ValidationError("deadline must be greater than now")
        return value


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)


class TaskDetailSerializer(serializers.ModelSerializer):
    # Задание 3: Использование вложенных сериализаторов
    # Создайте сериализатор для TaskDetailSerializer, который включает
    # вложенный сериализатор для полного отображения связанных подзадач (SubTask).
    # Сериализатор должен показывать все подзадачи, связанные с данной задачей.
    # Шаги для выполнения:
    # Определите TaskDetailSerializer в файле serializers.py.
    # Вложите SubTaskSerializer внутрь TaskDetailSerializer.
    subtasks = SubTaskCreateSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',]

    def create(self, validated_data):
        name = validated_data['name'].strip()
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError({'nameError': 'Category with this name already exists!'})
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
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



