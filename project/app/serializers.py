# app/serializers.py
from rest_framework import serializers
from .models import Category, Task

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "due_date",
            "notified",
            "category",
            "telegram_user_id",
        )
        read_only_fields = ("created_at", "notified")
