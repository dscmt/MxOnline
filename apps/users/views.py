# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import UserProfile
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 查询 user 是否存在
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:  #如果验证失败
            return None


def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(user_name=user_name, password=pass_word)  # 如果通过就是user类，不通过就是None
        if user is not None:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, "login.html", {"msg": u"用户名或密码错误"})

    elif request.method == "GET":
        return render(request, "login.html", {})
