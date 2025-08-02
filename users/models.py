from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime as dt


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='static/avatars/', blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    telegram_chat_id = models.CharField(max_length=50, verbose_name='Telegrm chat id', blank=True)

    """
    время по умолчанию напоминания о привычке на сегодня, если для нее отдельно время не установлено
    """
    dayly_notification_time = (
        models.TimeField(default=dt.now().time().replace(hour=8, minute=30),
                         verbose_name='Время по умолчанию ежедневного напоминания в телеграме о привычках'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["last_name", "first_name"]
        # permissions = [('can_block_user', 'Can block and unblock users'), ]
