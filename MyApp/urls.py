from django.urls import path, re_path
from MyApp import views
from django.conf import settings

urlpatterns = [
    re_path(r'signup', views.signup),
    re_path(r'login/$', views.user_login,name = 'user_login')
]
