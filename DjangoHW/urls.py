from django.urls import path
from . import views

app_name = 'DjangoHW'

urlpatterns = [
    # Endpoint for creating tasks
    path('api/tasks/', views.create_task, name='create_task'),

    # Endpoints for getting tasks
    path('api/tasks/list/', views.task_list, name='task_list'),
    path('api/tasks/<int:task_id>/', views.task_detail, name='task_detail'),

    # Endpoint for statistics
    path('api/tasks/statistics/', views.task_statistics, name='task_statistics'),

    # SubTask endpoints
    path('api/subtasks/', views.SubTaskListCreateView.as_view(), name='subtask_list_create'),
    path('api/subtasks/<int:subtask_id>/', views.SubTaskDetailUpdateDeleteView.as_view(),
         name='subtask_detail_update_delete'),
]
