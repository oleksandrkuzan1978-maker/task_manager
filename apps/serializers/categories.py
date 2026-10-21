from rest_framework import serializers
from apps.task.models import Category

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