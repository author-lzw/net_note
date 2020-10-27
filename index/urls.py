"""
    主页分布式路由
"""
from django.urls import path

from index import views

urlpatterns = [
    path("", views.index_view),
]
