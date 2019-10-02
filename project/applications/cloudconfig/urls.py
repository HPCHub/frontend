from django.urls import path

from .views import StartConfig


urlpatterns = [
    path('start_config/<str:pk>/', StartConfig.as_view(), name='StartConfig'),
]
