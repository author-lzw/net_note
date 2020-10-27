"""
    user 用户分布式路由
"""
from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_view),
    path("reg", views.reg_view),
    path("logout", views.logout_view),
]
