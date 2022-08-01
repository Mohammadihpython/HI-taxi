from rest_framework import serializers

from django.conf import settings

User = settings.AUTH_USER_MODEL


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'password', 'first_name', 'last_name', 'gender']


class UserLight(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'password', ]
