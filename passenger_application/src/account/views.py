from functools import partial
from django.shortcuts import render
from django.utils.crypto import get_random_string
from datetime import datetime
from rest_framework.generics import GenericAPIView

from .models import CustomUser, UserOTP
from rest_framework.permissions import AllowAny
from .serializer import UserLight
from .tasks import send_sms
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class LoginApiView(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserLight
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                print(validated_data)
                code = get_random_string(length=5, allowed_chars="0123456789")
                try:
                    user_otp = UserOTP.objects.create(
                        phone_number=validated_data.get("phone_number"),
                        code=code,
                        code_type=UserOTP.LOGIN,
                    )
                    response = send_sms.delay(
                        phone_number=validated_data.get("phone_number"),
                        code=code,
                        code_type=UserOTP.LOGIN
                    )
                    print(code)
                    print(response.status)
                    return Response({"msg: sms send a few second"}, status=status.HTTP_201_CREATED)
                except ValueError:
                    return Response("some problem happen ", status=status.HTTP_404_NOT_FOUND)
            return Response('msg:the data is not valid', status=status.HTTP_400_BAD_REQUEST)


class VerifyLogin(GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            code = request.data['code']
            phone_number = request.data['phone_number']

            try:
                user = UserOTP.objects.filter(phone_number=phone_number).first()
                print(user.code)
                print(user.code == code)
                if user.code == code:
                    if user.time_in_range(
                    ):
                        user.login()
                    else:
                        return Response("your code is exoire")
                else:
                     return Response("code is not correct")
            except ValueError:
                return Response({"msg: wrong data"},status = status.HTTP_404_NOT_FOUND)
