# app/tasks.py
import requests
from celery import shared_task
from django.conf import settings

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_task_notification(self, telegram_user_id, text, task_pk):
    """
    Вызывается в момент due_date: отправляет POST на /send_message
    и помечает в БД Task.notified=True.
    """
    try:
        payload = {"telegram_id": telegram_user_id, "text": text}
        response = requests.post(
            f"http://{settings.NOTIFICATION_API_HOST}:{settings.NOTIFICATION_API_PORT}/send_message",
            json=payload,
            timeout=10
        )
        response.raise_for_status()
    except Exception as exc:
        # Повторим в случае ошибки
        raise self.retry(exc=exc)

    # Помечаем уведомление как отправленное
    from .models import Task
    Task.objects.filter(pk=task_pk).update(notified=True)
