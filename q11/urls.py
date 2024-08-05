from django.urls import path
from .views import *

urlpatterns = [
    path('',Home , name= 'home'),
    path('login/',Login , name= 'login'),
    path('register/',Register , name= 'register'),
    path('forget_password/', ForgetPassword , name= 'forget_password'),
    path('change_password/<str:token>/', ChangePassword, name='change_password'),
    path('logout',Logout , name= 'logout'),
]
