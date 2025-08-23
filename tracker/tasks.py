"""
автоматизация уведомлений
каждый день в полночь формируется список привычек, о которых сегодня надо напомнить -
это спиоск задач по расписанию, где время указано в свойствах привычки или пользователя

"""
import datetime
import datetime as dt
from celery import shared_task

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
def create_scheduled_habit_notification(user, habits, today: datetime) -> None:
    """
    отложенная задача для формирования в фоновом режиме напоминания о привычке по расписаню
    """
    for habit in habits:
        send_telegram_message(user_id=user.id, habit_id=habit.id)
        # if not habit.notification_time:
        #     habit.notification_time = user.dayly_notification_time
        #     habit.save()
        #
        # if habit.notification_time:  # отправить сообщение в телегу один раз сегодня в указанное время
        #     time_to_run = datetime.datetime(today.year, today.month, today.day, habit.notification_time.minute,
        #                                     habit.notification_time.second)
        #     scheduled_telegram_habit_notification.apply_async(eta=time_to_run)


@shared_task
def prepare_dayly_notifications():
    """
    каждый день в полночь сервер создает задачи по расписанию для оповещения пользователей о привычках на текущий день
    """
    now = dt.datetime.now(dt.timezone.utc)
    today = now.date()


    for user in CustomUser.objects.all():
        dayly_habits = Habit.objects.filter(owner=user).filter(frequency=1).filter(notification_is_scheduled=False)

        for habit in dayly_habits:
            if not habit.notification_time:
                habit.notification_time = user.dayly_notification_time
                habit.save()
            if habit.notification_time:
                # send_telegram_message(user_id=user.id, habit_id=habit.id)
                time_to_run = datetime.datetime(today.year,
                                                today.month,
                                                today.day,
                                                habit.notification_time.hour,
                                                habit.notification_time.minute,
                                                habit.notification_time.second)
                # if ((now.hour < time_to_run.hour) and (now.minute < time_to_run.minute) and
                #         (now.second < time_to_run.second)):
                scheduled_telegram_habit_notification.apply_async(args=[user.id, habit.id], eta=time_to_run)
                habit.notification_is_scheduled = True
                habit.save()

        # create_scheduled_habit_notification.delay(user, dayly_habits, today)

        # non_dayly_habits = list(Habit.objects.filter(owner=user).exclude(frequency=1))
        #
        # for habit in non_dayly_habits:
        #     if not habit.start_date:
        #         continue
        #     delta = (today - habit.start_date).days
        #     if delta % habit.frequency:
        #         non_dayly_habits.remove(habit)
        #
        # create_scheduled_habit_notification.delay(non_dayly_habits, today)
