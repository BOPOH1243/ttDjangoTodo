# app/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from celery import current_app

from .models import Task
from .tasks import send_task_notification

@receiver(pre_save, sender=Task)
def revoke_previous_task(sender, instance: Task, **kwargs):
    # Только для обновлений, когда due_date меняется
    if not instance._state.adding:
        old = Task.objects.get(pk=instance.pk)
        if old.due_date != instance.due_date and old.scheduled_task_id:
            # Отзываем старую запланированную задачу
            current_app.control.revoke(old.scheduled_task_id, terminate=False)

@receiver(post_save, sender=Task)
def schedule_notification(sender, instance: Task, created, **kwargs):
    # Вычислим сообщение
    text = f"Задача «{instance.title}» должна быть выполнена к {instance.due_date:%Y-%m-%d %H:%M}."
    # Если задача уже уведомлена и due_date ещё в прошлом — ничего не делаем
    if instance.notified and instance.due_date <= timezone.now():
        return

    # Планируем новую таску на due_date
    result = send_task_notification.apply_async(
        args=[instance.telegram_user_id, text, instance.pk],
        eta=instance.due_date
    )
    # Сохраняем ID запланированной таски
    Task.objects.filter(pk=instance.pk).update(scheduled_task_id=result.id)
