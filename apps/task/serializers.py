from os import name

from rest_framework import serializers
from .models import Task, Category, SubTask

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        exclude = ('description',)
        read_only_fields = ('id',)


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SubTask
        fields = ('title', 'status', 'deadline')
        #read_only_fields = ('created_id',)



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



