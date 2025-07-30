from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


class CustomUserLoginOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class CustomUserSerializer(serializers.ModelSerializer):
    # payments = PaymentSerializer(source='Платежи', many=True, required=False)

    class Meta:
        model = CustomUser
        fields = '__all__'

    # def get_payments(self, obj):
    #     return obj.Платежи.order_by('-created_at')


class CustomUserRestrictedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'city']




# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # Добавление пользовательских полей в токен
#         token['username'] = user.username
#         token['email'] = user.email
#
#         return token


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    # old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
