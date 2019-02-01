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
from rbac.forms.menu import MenuForm,SecondMenuForm,PermissionForm
from rbac.service import url_pack


def menu_list(request):
    menus = Menu.objects.all().values() # 1
    menu_id = request.GET.get('mid')
    parent_id = request.GET.get('pid')
    menu2s = Permission.objects.filter(menu_id= menu_id).values() # 2
    permissions = Permission.objects.filter(pid_id=parent_id).values() # 3

    if not menu_id:
        menu2s = None
    else:
        for m1 in menus:
            print(m1)
            if m1['id'] == int(menu_id):
                m1['class'] = 'active'
    if not parent_id:
        permissions = None
    else:
        for m2 in menu2s:
            if m2['id'] == int(parent_id):
                m2['class'] = 'active'

    return render(request, 'rbac/menu_list.html',
                  {'menus': menus, 'menu2s': menu2s,
                   'permissions': permissions,
                   'request': request,
                   'mid': menu_id,
                   'pid': parent_id}
                  )

def menu_add(request):
    if request.method=='GET':
        form = MenuForm()
        return render(request,'rbac/change.html',{'form':form})
    form = MenuForm(data=request.POST)
    if form.is_valid():
        form.save()
        back = url_pack.url_param_unpack(request,'rbac:menu_list')
        return redirect(back)
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
        return redirect(url_pack.url_param_unpack(request, 'rbac:menu_list'))
    else:
        return render(request, 'rbac/change.html', {'form': form})

def menu_del(request,menu_id):
    menu = Menu.objects.filter(id=menu_id).first()
    if request.method == 'GET':
        msg = {'back': reverse('rbac:menu_list'), 'item': menu.title}
        return render(request, 'rbac/delete_warning.html', {'msg': msg})
    else:
        menu.delete()
        back = url_pack.url_param_unpack(request, 'rbac:menu_list')
        return redirect(back)

def second_menu_add(request,menu_id):
    if request.method == 'GET':
        menu = Menu.objects.filter(id=menu_id).first()
        if not menu:
            return HttpResponse('所属菜单不存在或已被删除')
        form = SecondMenuForm(initial={'menu':menu})
        return render(request, 'rbac/change.html',{'form':form})
    form = SecondMenuForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(url_pack.url_param_unpack(request,'rbac:menu_list'))
    else:
        return render(request, 'rbac/change.html', {'form': form})

def second_menu_edit(request, second_menu_id):
    obj = Permission.objects.filter(id=second_menu_id).first()
    if not obj:
        return HttpResponse('无此子菜单')
    if request.method == 'GET':
        form = SecondMenuForm(instance=obj)
        return render(request, 'rbac/change.html',{'form':form})
    form = SecondMenuForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(url_pack.url_param_unpack(request, 'rbac:menu_list'))
    else:
        return render(request, 'rbac/change.html', {'form': form})

def second_menu_del(request, second_menu_id):
    menu = Permission.objects.filter(id=second_menu_id).first()
    if request.method == 'GET':
        msg = {'back': url_pack.url_param_unpack(request, 'rbac:menu_list'), 'item': menu.title}
        return render(request, 'rbac/delete_warning.html', {'msg': msg})
    else:
        menu.delete()
        back = url_pack.url_param_unpack(request, 'rbac:menu_list')
        return redirect(back)

def permission_add(request,parent_id):
    if request.method == 'GET':
        parent = Permission.objects.filter(id=parent_id).first()
        if not parent:
            return HttpResponse('所关联的二级菜单不存在或已被删除')
        form = PermissionForm()
        form.instance.pid = parent
        msg = 'NOTE: 为二级菜单--“%s”--添加关联子权限'%parent.title
        return render(request, 'rbac/change.html', {'form': form,'msg':msg})
    form = PermissionForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(url_pack.url_param_unpack(request,'rbac:menu_list'))
    else:
        return render(request, 'rbac/change.html', {'form': form})

def permission_edit(request, permission_id):
    obj = Permission.objects.filter(id=permission_id).first()
    if not obj:
        return HttpResponse('无此子权限')
    if request.method == 'GET':
        form = PermissionForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = PermissionForm(data=request.POST,instance=obj)
    if form.is_valid():
        form.save()
        return redirect(url_pack.url_param_unpack(request,'rbac:menu_list'))
    else:
        return render(request, 'rbac/change.html', {'form': form})

def permission_del(request, permission_id):
    obj = Permission.objects.filter(id=permission_id).first()
    if request.method == 'GET':
        msg = {'back': url_pack.url_param_unpack(request, 'rbac:menu_list'), 'item': obj.title}
        return render(request, 'rbac/delete_warning.html', {'msg': msg})
    else:
        obj.delete()
        back = url_pack.url_param_unpack(request, 'rbac:menu_list')
        return redirect(back)

# ---------------------------------------------------------
def multi_permissions(request):
    pass
# todo


