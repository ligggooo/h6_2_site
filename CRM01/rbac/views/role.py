#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   role.py
@Time    :   2019/1/29 21:16
@Desc    :
'''
from django.shortcuts import HttpResponse,render,reverse,redirect
from rbac.models import *
from rbac.forms.role import RoleForm


def role_list(request):
    roles = Role.objects.all()
    return render(request, 'rbac/role_list.html', {'roles':roles})


def role_add(request):
    if request.method == 'GET':
        form = RoleForm()
        return render(request,'rbac/change.html', {'form': form})
    form_instance = RoleForm(request.POST)
    if form_instance.is_valid():
        form_instance.save()
        return redirect(reverse('rbac:role_list'))
    else:
        return render(request, 'rbac/change.html', {'form': form_instance})


def role_edit(request,role_id):
    role = Role.objects.filter(id=role_id).first()
    if not role:
        return HttpResponse('角色不存在')
    if request.method == 'GET':
        form = RoleForm(instance=role)
        return render(request,'rbac/change.html', {'form': form})
    form_instance = RoleForm(instance=role, data=request.POST)
    if form_instance.is_valid():
        form_instance.save()
        return redirect(reverse('rbac:role_list'))
    else:
        return render(request, 'rbac/change.html', {'form': form_instance})

def role_del(request,role_id):
    role = Role.objects.filter(id=role_id).first()
    if request.method == 'POST':
        role.delete()
        return redirect(reverse('rbac:role_list'))
    else:
        msg = {'back': reverse('rbac:role_list'), 'item': role.title}
        return render(request, 'rbac/delete_warning.html', {'msg': msg})
