from django.utils import timezone
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
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
        Get paginated list of all subtasks ordered by creation date (newest first)
        """
        subtasks = SubTask.objects.all().order_by('-created_at')
        
        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(subtasks, request)
        
        serializer = SubTaskSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
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


@api_view(['GET'])
def tasks_by_day_of_week(request):
    """
    Get tasks filtered by day of the week.
    If no day parameter is provided, returns all tasks.
    Accepts day parameter in Russian (e.g., 'вторник') or English (e.g., 'tuesday')
    """
    day_param = request.GET.get('day', None)
    
    # Mapping of day names to weekday numbers (Monday=0, Sunday=6)
    day_mapping = {
        # Russian
        'понедельник': 0, 'пн': 0,
        'вторник': 1, 'вт': 1,
        'среда': 2, 'ср': 2,
        'четверг': 3, 'чт': 3,
        'пятница': 4, 'пт': 4,
        'суббота': 5, 'сб': 5,
        'воскресенье': 6, 'вс': 6,
        # English
        'monday': 0, 'mon': 0,
        'tuesday': 1, 'tue': 1,
        'wednesday': 2, 'wed': 2,
        'thursday': 3, 'thu': 3,
        'friday': 4, 'fri': 4,
        'saturday': 5, 'sat': 5,
        'sunday': 6, 'sun': 6,
    }
    
    if day_param:
        day_param = day_param.lower().strip()
        if day_param not in day_mapping:
            return Response(
                {'error': 'Invalid day parameter. Use day names like "понедельник", "вторник", "monday", "tuesday", etc.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        target_weekday = day_mapping[day_param]
        tasks = Task.objects.filter(deadline__week_day=target_weekday + 1)  # Django uses 1-7 (Sunday=1)
    else:
        tasks = Task.objects.all()
    
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def subtasks_filtered(request):
    """
    Get filtered subtasks with pagination.
    Filters:
    - task_title: Filter by main task title (case-insensitive partial match)
    - status: Filter by subtask status
    
    Default behavior: Returns all subtasks with pagination.
    """
    task_title = request.GET.get('task_title', None)
    status_filter = request.GET.get('status', None)
    
    # Start with all subtasks, ordered by creation date (newest first)
    subtasks = SubTask.objects.all().order_by('-created_at')
    
    # Apply filters
    if task_title:
        # Filter by main task title (case-insensitive)
        subtasks = subtasks.filter(task__title__icontains=task_title)
    
    if status_filter:
        # Filter by subtask status
        subtasks = subtasks.filter(status__iexact=status_filter)
    
    # Apply pagination
    paginator = PageNumberPagination()
    paginator.page_size = 5
    result_page = paginator.paginate_queryset(subtasks, request)
    
    serializer = SubTaskSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


