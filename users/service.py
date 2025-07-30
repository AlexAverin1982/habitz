from rest_framework.generics import get_object_or_404

from config import settings
import requests

from tracker.models import Habit
from users.models import CustomUser


def send_telegram_message(user_id: int, habit_id: int = 0) -> None:
    # user = CustomUser.objects.get(pk=user_id)
    user = get_object_or_404(CustomUser, id=user_id)
    chat_id = user.telegram_chat_id

    if not settings.TELEGRAM_BOT_TOKEN:
        raise ValueError("Токен телеграм-бота отсутствует в настройках приложения")
    if not chat_id:
        raise ValueError("ID телеграм-чата трекера привычек отсутствует в настройках пользователя")

    url = f"{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    if habit_id:
        habit = get_object_or_404(Habit, id=habit_id)
        requests.get(url=url, params={'text': repr(habit), 'chat_id': chat_id})
    else:
        habits = Habit.objects.filter(owner=user)
        for habit in habits:
            requests.get(url=url, params={'text': repr(habit), 'chat_id': chat_id})
