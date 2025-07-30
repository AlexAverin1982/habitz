from django.urls import path
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshSlidingView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, CustomUserPartialUpdateAPIView, ChangePasswordView, \
    UserDeleteAPIView, CustomUserRetrieveAPIView, CustomUserTelegramNotifyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='materials:home'), name='logout'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('profile/<int:pk>/', CustomUserRetrieveAPIView.as_view(), name='profile'),
    path('', UserListAPIView.as_view(), name='users'),
    path("all/", UserListAPIView.as_view(), name='users_all', kwargs={"full": True}),
    path('edit/<int:pk>/', CustomUserPartialUpdateAPIView.as_view(), name='edit_user'),
    path('set_password/<int:pk>/', ChangePasswordView.as_view(), name='set_password'),
    path("delete/<int:pk>/", UserDeleteAPIView.as_view(), name="delete_user"),
    path('token_refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    path('tg_notify/<int:pk>/', CustomUserTelegramNotifyAPIView.as_view(), name='tg_notify'),
]
