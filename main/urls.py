from django.urls import path

from main.views import home, register, logout_action, custom_login

# todo! from common import views


urlpatterns = [
    path('', home, name='home'),
    path("register/", register, name="register"),
    path('logout/', logout_action, name='exit'),
    path("login/", custom_login, name="custom_login"),
]