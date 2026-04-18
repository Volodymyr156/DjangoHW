from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer


@api_view(['POST'])
def create_task(request):
    """
    Создание новой задачи
    """
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        task = serializer.save()
        response_serializer = TaskSerializer(task)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_list(request):
    """
    Получение списка всех задач
    """
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def task_detail(request, task_id):
    """
    Получение конкретной задачи по её ID
    """
    try:
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    except Task.DoesNotExist:
        return Response(
            {'error': 'Task not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def task_statistics(request):
    """
    Получение статистики задач:
    - Общее количество задач
    - Количество задач по каждому статусу
    - Количество просроченных задач
    """
    total_tasks = Task.objects.count()
    
    # Количество задач по каждому статусу
    status_counts = {}
    for status_choice in Task.STATUS_CHOICES:
        status_name = status_choice[0]
        count = Task.objects.filter(status=status_name).count()
        status_counts[status_name] = count
    
    # Количество просроченных задач (не выполненные и с истекшим дедлайном)
    current_time = timezone.now()
    overdue_tasks = Task.objects.filter(
        deadline__lt=current_time
    ).exclude(status='done').count()
    
    statistics = {
        'total_tasks': total_tasks,
        'tasks_by_status': status_counts,
        'overdue_tasks': overdue_tasks
    }
    
    return Response(statistics)
