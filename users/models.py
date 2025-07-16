from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from rest_framework.generics import get_object_or_404
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='static/avatars/', blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["last_name", "first_name"]
        # permissions = [('can_block_user', 'Can block and unblock users'), ]
