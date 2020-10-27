from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .models import Note
from user.models import User
import html


# Create your views here.
# 登录认证的装饰器
def login_check(fn):
    def wrap(request, *args, **kwargs):
        if "uname" not in request.session or "uid" not in request.session:
            c_uname = request.COOKIES.get("uname")
            c_uid = request.COOKIES.get("uid")
            if not c_uname or not c_uid:
                return HttpResponseRedirect("/user/login")
            else:
                # 重写session
                request.session["uname"] = c_uname
                request.session["uid"] = c_uid
        return fn(request, *args, **kwargs)

    return wrap


@login_check
def add_view(request):
    if request.method == "GET":
        return render(request, "note/add_note.html")
    elif request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        # 前后端分离,注意转义,防止xss攻击,Django模板自带转义
        # title = html.escape(title)
        # 获取外键uid
        uid = request.session["uid"]
        Note.objects.create(title=title, content=content, user_id=uid)
        return HttpResponse("添加云笔记成功")

