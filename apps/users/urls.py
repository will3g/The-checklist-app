from django.urls import path

from .views import *

urlpatterns = [
    path(route='register', view=register, name='register'),
    path(route='login', view=login, name='login'),
    path(route='logout', view=logout, name='logout'),
]
