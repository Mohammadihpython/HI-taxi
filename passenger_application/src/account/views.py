from django.shortcuts import render

from rest_framework.generics import GenericAPIView
from account.models import CustomUser
from rest_framework.permissions import AllowAny
from account.serializer import UserLight


class LoginApiView(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserLight
    permission_classes = [AllowAny,]

    def get_object(self):
        obj = CustomUser.objects.filter(
            phone_number=self.request.data['phone_number']).first()
        return obj
    def post(self,request,):
        if request.method == 'POST':
            user =self.get_object()
            serilizer = self.get_serializer(data=user, partial =True)
