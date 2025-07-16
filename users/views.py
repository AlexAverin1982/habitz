from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from dotenv import load_dotenv
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse

from .models import CustomUser
from rest_framework import generics, mixins, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .permissions import IsSuperUser, IsOwnProfile, IsAdmin
from .serializers import CustomUserSerializer, ChangePasswordSerializer, CustomUserRestrictedSerializer

User = get_user_model()
load_dotenv()


class UserCreateAPIView(generics.CreateAPIView):
    """
    Регистрация пользователя
    """
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserDeleteAPIView(generics.DestroyAPIView):
    """
    Удаление пользователя
    """
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsSuperUser | IsOwnProfile]


class UserListAPIView(ListAPIView):
    """
    Список пользователей
    """
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class CustomUserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Данные о пользователе, доступные всем зарегистривовавшимся
    """
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]  # , IsOwnProfile]

    def get_serializer_class(self):
        profile_id = self.kwargs.get('pk')
        if profile_id:
            if profile_id == self.request.user.id:
                return CustomUserSerializer
            else:
                return CustomUserRestrictedSerializer


class CustomUserPartialUpdateAPIView(generics.GenericAPIView, mixins.UpdateModelMixin):
    """
    Частичное обновление данных в своем профиле
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsOwnProfile]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ChangePasswordView(generics.UpdateAPIView):
    """
    Смена пароля
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = [IsAuthenticated, IsSuperUser | IsOwnProfile]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            # if not self.object.check_password(serializer.data.get("old_password")):
            #     return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            password = serializer.data.get("new_password")
            user = CustomUser.objects.get(pk=kwargs['pk'])
            user.set_password(password)
            user.save()
            # self.object.set_password(password)
            # self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#############################################################################################################
#
# class CreatePeriodicTaskCheckInactiveUsers(generics.GenericAPIView):
#     serializer_class = CustomUserSerializer
#     queryset = CustomUser.objects.all()
#
#     permission_classes = [IsAuthenticated, IsAdmin]
#
#     def post(self, request, *args, **kwargs):
#         from datetime import datetime as dt, timedelta
#         from users.admin_tools import enable_periodic_task
#         enable_periodic_task(every=20,
#                              period='seconds',
#                              name='check inactive users',
#                              task='users.tasks.check_inactive_users',
#                              expires=dt.now() + timedelta(seconds=30))
#
#         return Response({"status": 200, "message": "check task in admin tool"})