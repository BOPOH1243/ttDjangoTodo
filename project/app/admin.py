# app/admin.py
from django.contrib import admin
from .models import Category, Task

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "telegram_user_id", "due_date", "notified")
    list_filter = ("category", "notified")
    search_fields = ("title", "description", "telegram_user_id")
    readonly_fields = ("created_at",)
