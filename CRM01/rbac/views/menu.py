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
from rbac.forms.menu import MenuForm,SecondMenuForm,PermissionForm,\
    MultiAddPermissionForm,MultiAddPermissionUpdateForm
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
from django.forms import formset_factory

def multi_permissions_add(request):
    MultiAddPermissionFormSet = formset_factory(MultiAddPermissionForm, extra=4)
    if request.method == 'GET':
        formset = MultiAddPermissionFormSet()
        return render(request, 'rbac/multi_permission_add.html', {'formset': formset})
    else:
        formset = MultiAddPermissionFormSet(data=request.POST)
        print(formset.total_form_count())
        valid_flag = True
        for form in formset:
            if form.is_valid():
                if not form.cleaned_data:
                    continue
                try:
                    obj = Permission(**form.cleaned_data)
                    obj.validate_unique()
                    obj.save()
                except Exception as e:
                    form.errors.update(e)
                    valid_flag = False
            else:
                valid_flag = False
        if valid_flag:
            return HttpResponse('ok')
        else:
            return render(request, 'rbac/multi_permission_add.html', {'formset': formset})

def multi_permissions_edit(request):
    MultiAddPermissionFormSet = formset_factory(MultiAddPermissionUpdateForm, extra=0)
    if request.method == 'GET':
        formset = MultiAddPermissionFormSet(initial=Permission.objects.all().values())
        return render(request, 'rbac/multi_permission_add.html', {'formset': formset})
    else:
        formset = MultiAddPermissionFormSet(data=request.POST, initial=Permission.objects.all().values())
        # 因为初始字段的int和data字段的str差异，导致这个地方无法正确判断has_changed
        print(formset.total_form_count())
        valid_flag = True
        for form in formset:
            if form.is_valid() and form.has_changed():
                row = form.cleaned_data
                if not form.cleaned_data:
                    continue
                try:
                    permission_id = row.pop('id')
                    per_obj = Permission.objects.filter(id=permission_id).first()
                    print(row)
                    for k,v in row.items():
                        print(k,v)
                        setattr(per_obj,k,v)
                    per_obj.validate_unique()
                    per_obj.save()
                except Exception as e:
                    form.errors.update(e)
                    valid_flag = False
            else:
                valid_flag = False
        if valid_flag:
            return HttpResponse('ok')
        else:
            return render(request, 'rbac/multi_permission_add.html', {'formset': formset})

def multi_permissions(request):
    from rbac.service.url_search import find_all_urls
    post_type = request.GET.get('type')

    permissions_to_add_form = None
    permissions_to_edit_form = None

    if request.method == 'POST' and post_type == 'add':
        MultiAddPermissionFormSet = formset_factory(MultiAddPermissionForm, extra=0)
        formset = MultiAddPermissionFormSet(data=request.POST)
        valid_flag = True
        to_add = []
        for form in formset:
            if form.is_valid():
                if not form.cleaned_data:
                    continue
                try:
                    obj = Permission(**form.cleaned_data)
                    obj.validate_unique()
                    to_add.append(obj)
                except Exception as e:
                    form.errors.update(e)
                    valid_flag = False
            else:
                valid_flag = False
        if valid_flag:
            Permission.objects.bulk_create(to_add,batch_size=100)
        else:
            permissions_to_add_form = formset

    if request.method == 'POST' and post_type == 'edit':
        PermissionFormSet = formset_factory(MultiAddPermissionUpdateForm, extra=0)
        formset = PermissionFormSet(data=request.POST)
        valid_flag = True
        to_add = []
        for form in formset:
            if form.is_valid():
                row = form.cleaned_data
                if not form.cleaned_data:
                    continue
                try:
                    permission_id = row.pop('id')
                    per_obj = Permission.objects.filter(id=permission_id).first()
                    # print(row)
                    changed = False
                    for k, v in row.items():
                        # print(k, v)
                        v_new = getattr(per_obj,k)
                        if not v and not v_new:
                            continue
                        if str(v) != str(v_new):
                            setattr(per_obj, k, v)
                            changed = True
                    if changed:
                        per_obj.validate_unique()
                        per_obj.save()
                    else:
                        print('没变')
                except Exception as e:
                    form.errors.update(e)
                    valid_flag = False
            else:
                valid_flag = False
        if not valid_flag:
            permissions_to_edit_form = formset

    urls_in_project = find_all_urls()
    urls_in_db = Permission.objects.all()

    urls_in_project_set = set(urls_in_project.keys())
    urls_in_db_set = set(x['name'] for x in urls_in_db.values('name'))

    # To delete
    permissions_to_delete_set = urls_in_db_set - urls_in_project_set
    permissions_to_delete = [x for x in urls_in_db if x.name in permissions_to_delete_set]

    # To add
    if not permissions_to_add_form:
        permissions_to_add_set = urls_in_project_set - urls_in_db_set
        permissions_to_add = [{'name':x[0],'url':x[1]} for x in urls_in_project.items() if x[0] in permissions_to_add_set]
        MultiAddPermissionFormSet = formset_factory(MultiAddPermissionForm, extra=0)
        permissions_to_add_form = MultiAddPermissionFormSet(initial=permissions_to_add)


    # To update
    if not permissions_to_edit_form:
        permissions_to_update_set = urls_in_project_set & urls_in_db_set
        permissions_to_update = urls_in_db.filter(name__in=permissions_to_update_set).values()
        MultiEditPermissionFormSet = formset_factory(MultiAddPermissionUpdateForm, extra=0)
        permissions_to_edit_form = MultiEditPermissionFormSet(initial=permissions_to_update)
    return render(request, 'rbac/permissions_change.html', locals())


def multi_permission_del(request, permission_id):
    obj = Permission.objects.filter(id=permission_id).first()
    if obj:
        obj.delete()
    back = url_pack.url_param_unpack(request, 'rbac:multi_permissions')
    return redirect(back)
