from rest_framework import serializers

from django.conf import settings
from . models import CustomUser

User = settings.AUTH_USER_MODEL


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'password', 'first_name', 'last_name', 'gender']


class UserLight(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'password']

    def validate(self, data) :
        phone_number = data.get('phone_number')
        
        password = data.get('password')
        user = CustomUser.objects.filter(phone_number=phone_number).first()
        if user:
            if user.password == password:
                return data

            else:
                raise serializers.ValidationError('password wrong!')
        raise serializers.ValidationError('phone number didnt exist!')
