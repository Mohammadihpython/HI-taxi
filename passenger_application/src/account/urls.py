from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginApiView.as_view(), name="login"),
    path('verifylog/', views.VerifyLogin.as_view(), name="login-verify"),
    path('register/', views.RegisterView.as_view(), name="register"),

]
