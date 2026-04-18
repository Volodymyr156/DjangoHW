from django.urls import path
from . import views

app_name = 'DjangoHW'

urlpatterns = [
    # Эндпоинт для создания задачи
    path('api/tasks/', views.create_task, name='create_task'),

    # Эндпоинты для получения задач
    path('api/tasks/list/', views.task_list, name='task_list'),
    path('api/tasks/<int:task_id>/', views.task_detail, name='task_detail'),

    # Эндпоинт для статистики
    path('api/tasks/statistics/', views.task_statistics, name='task_statistics'),
]