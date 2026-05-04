from django.urls import path

from .views import trigger_sync

urlpatterns = [
    path("sync/", trigger_sync),
]