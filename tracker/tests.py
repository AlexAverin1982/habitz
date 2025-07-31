"""
test crud for habits
"""
import datetime
from dateutil.utils import today
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from users.models import CustomUser
from tracker.models import Location, Action, Reward, Habit

client = APIClient()


class HabitTestCase(APITestCase):

    def setUp(self):
        # self.user = CustomUser.objects.create(email='test@example.com')
        #
        self.su = CustomUser.objects.create_user(username="su", email="su@mail.ru", password='123456')
        self.su.is_active = True
        self.su.is_admin = True
        self.su.is_superuser = True
        self.su.save()

        self.user_1 = CustomUser.objects.create_user(username="user_1", email="user1@mail.ru", password='123456')
        self.user_1.is_active = True
        self.user_1.is_admin = False
        self.user_1.is_superuser = False
        self.user_1.save()

        self.user_2 = CustomUser.objects.create_user(username="user_2", email="user2@mail.ru", password='123456')
        self.user_2.is_active = True
        self.user_2.is_admin = False
        self.user_2.is_superuser = False
        self.user_2.save()

        self.location_1 = Location.objects.create(name='location_1', owner=self.user_1)
        self.location_2 = Location.objects.create(name='location_2', owner=self.user_1, preposition='in a')
        self.action_1 = Action.objects.create(name='action_1', owner=self.user_1)
        self.reward_1 = Reward.objects.create(name='reward_1', owner=self.user_1)

    def test_habit_CRUD(self):
        useful_habit_1 = Habit.objects.create(name='useful_habit_1',
                                              owner=self.user_1,
                                              location=self.location_1,
                                              action=self.action_1,
                                              time=datetime.time(hour=18, minute=15),
                                              is_pleasant=False)

        pleasant_habit_1 = Habit.objects.create(name='pleasant_habit_1',
                                                owner=self.user_1,
                                                location=self.location_2,
                                                action=self.action_1,
                                                time=datetime.time(hour=18, minute=15),
                                                is_pleasant=True)

        useful_habit_1.chain_habit = pleasant_habit_1
        useful_habit_1.save()

        # useful_habit_2 = Habit.objects.create(name='useful_habit_2',
        #                                       owner=self.user_1,
        #                                       location=self.location_1,
        #                                       action=self.action_1,
        #                                       time=datetime.time(hour=10, minute=30),
        #                                       is_pleasant=False,
        #                                       reward=self.reward_1)

        client.force_authenticate(user=self.user_1)
        data = {"reward": self.reward_1.id}
        response = client.put(f'/edit_habit/{useful_habit_1.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['non_field_errors'][0], "Для привычки уже указана привязанная привычка")

        # data = {"chain_reward": ''}
        # response = client.put(f'/edit_habit/{useful_habit_1.id}/', data=data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        useful_habit_1.chain_habit = None
        useful_habit_1.save()

        data = {"reward": self.reward_1.id}
        response = client.put(f'/edit_habit/{useful_habit_1.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"reward": self.reward_1.id, "chain_habit": pleasant_habit_1.id}
        response = client.put(f'/edit_habit/{useful_habit_1.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # print(response.json())
        self.assertEqual(response.json()['non_field_errors'][0],
                         "Неправильно указывать для привычки одновременно награду и связанную привычку")

        data = {"frequency": 7}
        response = client.put(f'/edit_habit/{useful_habit_1.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['frequency'][0], "Ensure this value is less than or equal to 6.")

        useful_habit_1.start_date = None
        useful_habit_1.save()

        data = {"frequency": 6}
        response = client.put(f'/edit_habit/{useful_habit_1.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['non_field_errors'][0],
                         "Требуется указать начальную дату для не ежедневной привычки.")

        data = {"frequency": 6, "start_date": (today() + datetime.timedelta(hours=36)).date()}
        response = client.put(f'/edit_habit/{useful_habit_1.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {"chain_habit": pleasant_habit_1.id}
        response = client.put(f'/edit_habit/{pleasant_habit_1.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # print(response.json())
        self.assertEqual(response.json()['non_field_errors'][0],
                         "К приятной привычке нельзя привязывать никакую другую привычку")

        self.assertEqual(str(self.location_1), self.location_1.name)
        self.assertEqual(str(self.action_1), self.action_1.name)
        self.assertEqual(str(self.reward_1), self.reward_1.name)
        h = Habit.objects.get(id=useful_habit_1.id)
        # print(f"h: {repr(h)}")
        self.assertEqual(str(h),
                         f"Я буду {h.action.name} в {h.time} {h.location.name} через каждые {h.frequency} дней")

        h.frequency = 4
        h.save()
        self.assertEqual(str(h),
                         f"Я буду {h.action.name} в {h.time} {h.location.name} через каждые {h.frequency} дня")

        self.assertEqual(repr(h), f"{h.action.name} в {h.time} {h.location.name}")

        h = Habit.objects.get(id=pleasant_habit_1.id)
        self.assertEqual(str(h),
                         f"Я буду {h.action.name} в {h.time} {h.location.preposition} {h.location.name} ежедневно")
        self.assertEqual(repr(h),
                         f"{h.action.name} в {h.time} {h.location.preposition} {h.location.name}")

        assert True
