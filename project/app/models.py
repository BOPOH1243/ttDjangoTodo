# app/models.py
from django.db import models
from django.utils import timezone
from .utils import generate_pk
import hashlib
import json
from datetime import date, datetime

class GenerateIDMixin(models.Model):
    """
    Абстрактный миксин для генерации первичного ключа.
    При сериализации дат конвертирует их в строки ISO,
    а для внешних ключей берет поле id связанной модели.
    """
    class Meta:
        abstract = True

    id = models.CharField(
        primary_key=True,
        max_length=64,  # длина SHA-256 в hex
        editable=False,
        unique=True,
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            stable_fields = {}
            for field in self._meta.fields:
                name = field.name
                # Пропускаем само поле id и метки времени
                if name == 'id' or name in ('created_at', 'updated_at'):
                    continue

                value = getattr(self, name)

                # Если внешний ключ или любая модель, берем его id
                if hasattr(value, 'pk') and hasattr(value, 'id'):
                    value = value.id

                # Преобразуем даты/время в строку
                if isinstance(value, (datetime, date)):
                    value = value.isoformat()

                stable_fields[name] = value

            # Сериализуем в JSON с сортировкой ключей
            json_str = json.dumps(
                stable_fields,
                sort_keys=True,
                separators=(',', ':'),
                ensure_ascii=False,
            )

            # Генерируем SHA-256 хеш
            self.id = hashlib.sha256(json_str.encode('utf-8')).hexdigest()

        super().save(*args, **kwargs)

class Category(GenerateIDMixin):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Task(GenerateIDMixin):
    title = models.CharField("Заголовок", max_length=200)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    due_date = models.DateTimeField("Срок исполнения")
    notified = models.BooleanField(
        "Уведомление отправлено", default=False,
        help_text="Ставить True после отправки уведомления через Celery"
    )
    # привязка к категории и «телеграм-ID» пользователя
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        related_name="tasks", verbose_name="Категория"
    )
    telegram_user_id = models.BigIntegerField(
        "Telegram User ID",
        help_text="Числовой идентификатор пользователя в Telegram"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.category})"
