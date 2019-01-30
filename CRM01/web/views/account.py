#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse, render, redirect,reverse

from rbac import models
from rbac.service.init_permission import init_permission




def login(request):
    # 1. 用户登录
    if request.method == 'GET':
        request.session.flush()
        return render(request, 'login.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')

    current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not current_user:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})

    init_permission(current_user, request)

    return redirect('/customer/list/')

def logout(request):
    request.session.flush()
    return redirect(reverse('web:login'))
