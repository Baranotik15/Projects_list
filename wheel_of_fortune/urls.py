from django.urls import path
from . import views

urlpatterns = [
    path('', views.wheel_of_fortune, name='wheel_of_fortune'),
]
