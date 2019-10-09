from django.urls import path

from .views import StartConfig, LaunchHistoryStatus, GetKeyFile


urlpatterns = [
    path('start_config/<str:pk>/', StartConfig.as_view(), name='StartConfig'),
    path('get_status/<str:pk>/', LaunchHistoryStatus.as_view(), name='LaunchHistoryStatus'),
    path('keyfile/<str:pk>/', GetKeyFile.as_view(), name='GetKeyFile'),

]
