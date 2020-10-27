from django.shortcuts import render

# Create your views here.

"""
    主页应用视图函数
"""


def index_view(request):
    return render(request, "index/index.html")
