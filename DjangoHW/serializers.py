from rest_framework import serializers
from .models import Task, Category


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
