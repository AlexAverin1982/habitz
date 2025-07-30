"""
test crud for habits
"""
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from users.models import CustomUser

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

        # self.location_1 = Location.objects.create(name='location_1', owner=self.user_1)
        # self.location_2 = Location.objects.create(name='location_2', owner=self.user_1, preposition='in a')
        # self.action_1 = Action.objects.create(name='action_1', owner=self.user_1)
        # self.reward_1 = Reward.objects.create(name='reward_1', owner=self.user_1)

    def test_users_CRUD(self):
        self.assertEqual(str(self.user_1), self.user_1.email)
