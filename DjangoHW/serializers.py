from rest_framework import serializers
from django.utils import timezone
from .models import Task, Category, SubTask


class TaskSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'created_date', 'categories']
        read_only_fields = ['id', 'created_at', 'created_date']


class TaskCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'categories']
    
    def validate_deadline(self, value):
        """
        Validate that deadline is not in the past
        """
        if value < timezone.now():
            raise serializers.ValidationError(
                'Deadline cannot be in the past.'
            )
        return value


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = SubTask
        fields = ['title', 'description', 'task', 'status', 'deadline', 'created_at']


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True, read_only=True)
    subtasks = SubTaskSerializer(many=True, read_only=True, source='subtasks.all')
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'created_date', 'categories', 'subtasks']
        read_only_fields = ['id', 'created_at', 'created_date']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
    
    def create(self, validated_data):
        name = validated_data.get('name')
        
        # Check if category with this name already exists
        if Category.objects.filter(name__iexact=name).exists():
            raise serializers.ValidationError({
                'name': 'Category with this name already exists.'
            })
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        name = validated_data.get('name')
        
        # Check if another category with this name already exists
        if name and name.lower() != instance.name.lower():
            if Category.objects.filter(name__iexact=name).exclude(id=instance.id).exists():
                raise serializers.ValidationError({
                    'name': 'Category with this name already exists.'
                })
        
        return super().update(instance, validated_data)
