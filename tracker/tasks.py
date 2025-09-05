"""
автоматизация уведомлений
каждый день периодически формируется список привычек, о которых сегодня надо напомнить -
это список задач по расписанию, где время указано в свойствах привычки или пользователя

"""
import datetime
import datetime as dt

import requests
from celery import shared_task
from rest_framework.generics import get_object_or_404

from config import settings
from config.celery import app
from users.models import CustomUser
from tracker.models import Habit
from users.service import send_telegram_message

utc_delta = datetime.datetime.now().astimezone().tzinfo.utcoffset(datetime.datetime.now())


@app.task
def scheduled_telegram_habit_notification(user_id, habit_id):
    """
    отправить сообщение в телегу один раз сегодня в указанное время
    """
    send_telegram_message(user_id=user_id, habit_id=habit_id)
    habit = Habit.objects.get(id=habit_id)
    habit.notification_is_scheduled = False
    habit.save()


@shared_task
def prepare_dayly_notifications():
    """
    периодически в течение дня сервер просматривает, какие оповещения о привычках на текущий день
    сегодня надо отправить и создает соответствующие отложенные задачи отпавки сообщения в телегорамм-бот
    """

    def process_habits(habits) -> None:
        # send_telegram_message(1, 1, str(len(dayly_habits)) + ' habits in')
        for h in habits:

            if not h.notification_time:
                h.notification_time = user.dayly_notification_time
                h.save()

            time_to_run = datetime.datetime(today.year,
                                            today.month,
                                            today.day,
                                            h.notification_time.hour,
                                            h.notification_time.minute,
                                            h.notification_time.second)

            if ((now.hour <= time_to_run.hour) and (now.minute <= time_to_run.minute) and
                    (now.second <= time_to_run.second)):
                scheduled_telegram_habit_notification.apply_async(args=[user.id, h.id], eta=time_to_run)
                h.notification_is_scheduled = True
                h.save()

    now = dt.datetime.now(dt.timezone.utc)
    today = now.date()

    for user in CustomUser.objects.all():

        user_habits = Habit.objects.filter(owner=user)
        dayly_habits = user_habits.filter(frequency=1).filter(notification_is_scheduled=False)
        process_habits(dayly_habits)

        non_dayly_habits = user_habits.exclude(frequency=1).filter(notification_is_scheduled=False)

        for habit in non_dayly_habits:
            if not habit.start_date:
                continue
            delta = (today - habit.start_date).days
            if delta % habit.frequency:
                non_dayly_habits.remove(habit)

        process_habits(non_dayly_habits)
