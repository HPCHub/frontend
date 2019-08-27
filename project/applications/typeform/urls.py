from django.urls import path

from .views import TypeformViewSet


urlpatterns = [
    path('hook/', TypeformViewSet.as_view(), name='typeform_hook'),
]
