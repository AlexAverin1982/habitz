from django.db import models
from datetime import datetime as dt

"""
Привычка:
Пользователь — создатель привычки.
Место — место, в котором необходимо выполнять привычку.
Время — время, когда необходимо выполнять привычку.
Действие — действие, которое представляет собой привычка.
Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки.
Связанная привычка — привычка, которая связана с другой привычкой, важно указывать для полезных привычек,
но не для приятных.
Периодичность (по умолчанию ежедневная) — периодичность выполнения привычки для напоминания в днях.
Вознаграждение — чем пользователь должен себя вознаградить после выполнения.
Время на выполнение — время, которое предположительно потратит пользователь на выполнение привычки.
Признак публичности — привычки можно публиковать в общий доступ,
чтобы другие пользователи могли брать в пример чужие привычки.
"""


class Location(models.Model):
    """
    Место — место, в котором необходимо выполнять привычку.
    """
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(max_length=2000, verbose_name="Описание", blank=True)
    preposition = models.CharField(max_length=10, verbose_name="Предлог", blank=True)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, related_name='locations', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Место, в котором необходимо выполнять привычку"
        verbose_name_plural = "места"
        ordering = ["name"]
        # permissions = [('can_block_user', 'Can block and unblock users'), ]


class Action(models.Model):
    """
    Действие — действие, которое представляет собой привычка.
    """
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(max_length=2000, verbose_name="Описание", blank=True)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, related_name='actions', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Действие — действие, которое представляет собой привычка"
        verbose_name_plural = "действия"
        ordering = ["name"]
        # permissions = [('can_block_user', 'Can block and unblock users'), ]


class Reward(models.Model):
    """
    Вознаграждение — чем пользователь должен себя вознаградить после выполнения.
    """
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(max_length=2000, verbose_name="Описание", blank=True)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, related_name='rewards', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вознаграждение — чем пользователь должен себя вознаградить после выполнения"
        verbose_name_plural = "вознаграждение"
        ordering = ["name"]
        # permissions = [('can_block_user', 'Can block and unblock users'), ]


class Habit(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(max_length=2000, verbose_name="Описание", blank=True)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, related_name='my_habits',
                              verbose_name='Владелец привычки', null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, verbose_name='где выполнять привычку',
                                 blank=True, related_name='habit_locations', null=True)
    action = models.ForeignKey(Action, on_delete=models.SET_NULL, verbose_name='что представляет собой привычка',
                               blank=True, related_name='habit_actions', null=True)
    reward = models.ForeignKey(Reward, on_delete=models.SET_NULL, blank=True, related_name='habit_rewarded', null=True,
                               verbose_name='чем пользователь должен себя вознаградить после выполнения')

    time = models.TimeField(verbose_name='когда необходимо выполнять привычку', blank=True)
    start_date = models.DateField(verbose_name='дата начала выполнения для не ежедневных привычек', auto_now_add=True,
                                  blank=True, null=True)

    """
    время по умолчанию напоминания о привычке на сегодня
    """
    notification_time = models.TimeField(verbose_name='Время напоминания в телеграме',
                                         default=dt.now().time().replace(hour=8, minute=30))

    is_pleasant = models.BooleanField(verbose_name='Признак приятной привычки', default=True)
    is_public = models.BooleanField(verbose_name='Признак публичности', default=False)

    # TODO валидатор привязывания приятной привычки к полезной, но не наоборот + взаимное исключение
    # вознаграждения и привязанной привычки
    chain_habit = models.ForeignKey('self', verbose_name='Связанная привычка', on_delete=models.SET_NULL,
                                    blank=True, null=True)

    # TODO валидатор периодичности
    frequency = models.IntegerField(verbose_name='Периодичность выполнения привычки в днях', default=1)

    # TODO валидатор продолжительности
    duration = models.IntegerField(verbose_name='Время на выполнение в секундах', default=120)

    def __str__(self):
        result = f"Я буду {self.action.name} в {self.time}"
        if self.location.preposition:
            result += f" {self.location.preposition}"
        result += f" {self.location.name}"
        if self.frequency == 1:
            result += ' ежедневно'
        elif self.frequency < 5:
            result += f' через каждые {self.frequency} дня'
        else:
            result += f' через каждые {self.frequency} дней'
        return result.replace('  ', ' ')

    def __repr__(self):
        result = f"{self.action.name} в {self.time}"
        if self.location.preposition:
            result += f" {self.location.preposition}"
        result += f" {self.location.name}"
        return result.replace('  ', ' ')

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "привычки"
        ordering = ["name"]
