#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   menu.py
@Time    :   2019/1/30 19:24
@Desc    :
'''
from django.shortcuts import HttpResponse,render,reverse,redirect
from rbac.models import *
from rbac.forms.menu import MenuForm


def menu_list(request):
    menus = Menu.objects.all()
    return render(request, 'rbac/menu_list.html',{'menus':menus})

def menu_add(request):
    if request.method=='GET':
        form = MenuForm()
        return render(request,'rbac/change.html',{'form':form})
    form = MenuForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:menu_list'))
    else:
        return render(request, 'rbac/change.html', {'form': form})

def menu_edit(request,menu_id):
    menu = Menu.objects.filter(id=menu_id).first()
    if not menu:
        return HttpResponse('无此菜单')
    if request.method == 'GET':
        form = MenuForm(instance=menu)
        return render(request,'rbac/change.html',{'form':form})
    form = MenuForm(instance=menu, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:menu_list'))
    else:
        return render(request, 'rbac/change.html', {'form': form})

def menu_del(request,menu_id):
    menu = Menu.objects.filter(id=menu_id).first()
    if request.method=='GET':
        msg = {'back': reverse('rbac:menu_list'), 'item': menu.title}
        return render(request, 'rbac/delete_warning.html', {'msg': msg})
    else:
        menu.delete()
        return redirect(reverse('rbac:menu_list'))



# ---------------------------------------------------------
def multi_permissions(request):
    pass
# todo


