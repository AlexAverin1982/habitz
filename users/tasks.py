from celery import shared_task
from users.models import CustomUser
from users.service import send_telegram_message
from django.shortcuts import get_object_or_404


@shared_task
def habit_reminder(habit_id: int):
    habit = get_object_or_404(CustomUser, id=habit_id)
    send_telegram_message(habit.owner.id, habit_id)
