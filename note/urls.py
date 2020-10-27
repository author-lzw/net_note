from django.urls import path
from . import views

urlpatterns = [
    # 云笔记列表展示
    path("", views.list_view),
    # 云笔记添加
    path("add", views.add_view),
    # 云笔记修改
    path("mod/<int:uid>", views.mod_view),
    # 云笔记删除
    path("del/<int:uid>", views.del_view),
]
