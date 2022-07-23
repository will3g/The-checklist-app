from django.urls import path

from .views import *

urlpatterns = [
    path(route='', view=index, name='index'),
    path(route='dashboard', view=dashboard, name='dashboard'),
    path(route='new/task', view=new_task, name='new_task'),
    path(route='edit/task', view=edit_task, name='edit_task'),
    path(route='task/<int:task_id>', view=my_task, name='my_task'),
]
