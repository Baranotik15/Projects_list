from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("task/<int:pk>/", views.task_detail, name="task_detail"),
    path("add_task/", views.add_task, name="add_task"),
    path("toggle_task/<int:pk>/", views.toggle_task, name="toggle_task"),
    path("delete_task/<int:pk>/", views.delete_task, name="delete_task"),
]
