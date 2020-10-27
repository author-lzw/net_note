from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User
import hashlib


# Create your views here.

# 登录
def login_view(request):
    if request.method == "GET":
        # 检查session数据,来判断用户是否登录过
        if "uname" in request.session and "uid" in request.session:
            username = request.session["uname"]
            return render(request, "index/login_after.html", locals())
            # return HttpResponse("您已经登录")
        c_uname = request.COOKIES.get("uname")
        c_id = request.COOKIES.get("uid")
        print(c_id, c_uname)
        if c_uname and c_id:
            # cookies中的数据回写session
            request.session["uname"] = c_uname
            request.session["id"] = c_id
            # -------------------此处进不来--------------
            return HttpResponse("您已经登录")
        return render(request, "user/login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 为空检查
        if not username or not password:
            return HttpResponse("用户名密码不能为空")
        # 获取对象
        try:
            old_user = User.objects.get(username=username)
        except Exception as e:
            print("the error is %s" % e)
            return HttpResponse("用户名或密码错误")
        # 计算登录口令Hash
        md5 = hashlib.md5()
        md5.update(password.encode())
        password_h = md5.hexdigest()
        if password_h != old_user.password:
            return HttpResponse("用户名或密码错误")
        # 在session保存登录状态(信息)
        request.session["uname"] = old_user.username
        request.session["uid"] = old_user.id
        resp = HttpResponse("登录成功")
        # 若用户选择了记住我,还要在cookies中保存登录状态
        if "remember" in request.POST:
            print("------------------------")
            resp.set_cookie("uname", old_user.username, 3600 * 24 * 3)
            resp.set_cookie("uid", old_user.id, 3600 * 24 * 3)
        # 满足以上条件,则登录成功
        return render(request, "index/login_after.html", locals())
        # return HttpResponse("登录成功")


# 注册
def reg_view(request):
    if request.method == "GET":
        return render(request, "user/register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password_1 = request.POST.get("password_1")
        password_2 = request.POST.get("password_2")
        # 1.进行为空检查
        if not username or not password_1:
            return HttpResponse("用户名和密码允许为空")
        # 2.检测两次密码是否一直
        if password_1 != password_2:
            return HttpResponse("两次密码不一致")
        # 3.用户名是否被占用(导入模型类进行数据库数据查询)
        old_user = User.objects.filter(username=username)
        if old_user:
            return HttpResponse("用户名已存在!")
        # 4.是否会直接保存输入的'密码'呢？(保存口令的散列哈希算法值)
        md5 = hashlib.md5()  # 创建一个md5对象
        md5.update(password_1.encode())
        # 口令的hash值
        password_h = md5.hexdigest()
        # 添加数据进入数据库
        try:
            User.objects.create(username=username, password=password_h)
        except Exception as e:
            return HttpResponse("用户名已存在")
        return HttpResponseRedirect("/index")


# 注销
def logout_view(request):
    # 清除session登录状态
    if "uname" in request.session:
        del request.session["uname"]
    if "uid" in request.session:
        del request.session["uid"]
    # 清除cookies登录状态
    resp = HttpResponse("注销用户成功")
    resp.delete_cookie("uname")
    resp.delete_cookie("uid")
    return HttpResponseRedirect("/index")
