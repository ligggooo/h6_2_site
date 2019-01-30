#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   init_permission.py
@Time    :   2019/1/28 21:53
@Desc    :
'''
from django.conf import settings


def init_permission(current_user,request):
    permission_queryset = current_user.roles.filter(permissions__isnull=False).distinct().\
        values('permissions__id', 'permissions__name', 'permissions__title', 'permissions__url', 'permissions__pid__id',
               'permissions__pid__title', 'permissions__pid__url', 'permissions__pid__name',
               'permissions__menu__id', 'permissions__menu__title',
               'permissions__menu__icon')
    menu_tree = {}
    permission_dict = {}
    for item in permission_queryset:
        # 权限控制中间件
        permission_dict[item['permissions__name']] = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'name': item['permissions__name'],
            'parent_id': item['permissions__pid__id'],
            'parent_title': item['permissions__pid__title'],
            'parent_url': item['permissions__pid__url'],
            'parent_name': item['permissions__pid__name'],
        }
        # 渲染菜单用 建立菜单树
        menu_id = item['permissions__menu__id']
        if not menu_id:
            continue
        else:
            new_node = {'id' :item['permissions__id'],
                        'url': item['permissions__url'],
                        'title': item['permissions__title'],
                        'name': item['permissions__name']}
            if menu_id not in menu_tree:
                menu_tree[menu_id]={'title':item['permissions__menu__title'],
                                    'icon': item['permissions__menu__icon'],
                                    'subs':[new_node,]}
            else:
                menu_tree[menu_id]['subs'].append(new_node)

    request.session[settings.RBAC_MENU_KEY] = menu_tree
    request.session[settings.RBAC_PERMISSION_KEY] = permission_dict
