from rest_framework.generics import get_object_or_404

from config import settings
import requests

from tracker.models import Habit
from users.models import CustomUser
from datetime import datetime as dt


utc_delta = dt.now().astimezone().tzinfo.utcoffset(dt.now())

def send_telegram_message(user_id: int, habit_id, text: str = '') -> None:
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
        if text:
            requests.get(url=url, params={'text': text, 'chat_id': chat_id})
        else:
            requests.get(url=url, params={'text': repr(habit), 'chat_id': chat_id})
    else:
        habits = Habit.objects.filter(owner=user)
        for habit in habits:
            requests.get(url=url, params={'text': repr(habit), 'chat_id': chat_id})


def local_time_to_utc(local_time: str) -> str:
    c = local_time.count(':')
    if c == 1:
        format_str = '%H:%M'
    else:
        format_str = '%H:%M:%S'

    local_time = dt.strptime(local_time, format_str)
    return dt.strftime(local_time - utc_delta, format_str)
