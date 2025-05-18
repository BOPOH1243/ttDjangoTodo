# app/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CategoryViewSet, TaskViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("api/", include(router.urls)),
]
