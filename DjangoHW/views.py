from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task, SubTask
from .serializers import TaskSerializer, TaskCreateSerializer, SubTaskSerializer, SubTaskCreateSerializer


@api_view(['POST'])
def create_task(request):
    """
    Create a new task
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
    Get list of all tasks
    """
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def task_detail(request, task_id):
    """
    Get a specific task by its ID
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
    Get task statistics:
    - Total number of tasks
    - Number of tasks by each status
    - Number of overdue tasks
    """
    total_tasks = Task.objects.count()
    
    # Number of tasks by each status
    status_counts = {}
    for status_choice in Task.STATUS_CHOICES:
        status_name = status_choice[0]
        count = Task.objects.filter(status=status_name).count()
        status_counts[status_name] = count
    
    # Number of overdue tasks (not completed with expired deadline)
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


class SubTaskListCreateView(APIView):
    """
    View for creating and listing SubTasks
    """
    
    def get(self, request):
        """
        Get list of all subtasks
        """
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a new subtask
        """
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            subtask = serializer.save()
            response_serializer = SubTaskSerializer(subtask)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    """
    View for retrieving, updating and deleting a specific SubTask
    """
    
    def get_object(self, subtask_id):
        try:
            return SubTask.objects.get(id=subtask_id)
        except SubTask.DoesNotExist:
            return None
    
    def get(self, request, subtask_id):
        """
        Get a specific subtask by ID
        """
        subtask = self.get_object(subtask_id)
        if subtask is None:
            return Response(
                {'error': 'SubTask not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)
    
    def put(self, request, subtask_id):
        """
        Update a specific subtask
        """
        subtask = self.get_object(subtask_id)
        if subtask is None:
            return Response(
                {'error': 'SubTask not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = SubTaskCreateSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            updated_subtask = serializer.save()
            response_serializer = SubTaskSerializer(updated_subtask)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, subtask_id):
        """
        Delete a specific subtask
        """
        subtask = self.get_object(subtask_id)
        if subtask is None:
            return Response(
                {'error': 'SubTask not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
