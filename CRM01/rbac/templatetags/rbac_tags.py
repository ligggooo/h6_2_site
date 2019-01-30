#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   rbac_tags.py
@Time    :   2019/1/29 13:13
@Desc    :
'''
from collections import OrderedDict

from django.template import Library
from django.shortcuts import reverse
from django.conf import settings
from django.urls.exceptions import NoReverseMatch
register = Library()


@register.inclusion_tag('rbac/dynamic_left_menu.html')
def menu_list(request):
    current_pid = request.current_selected_permission_id
    menu_dict_0 = request.session.get(settings.RBAC_MENU_KEY)
    menu_dict = OrderedDict()
    for menu_id in sorted(menu_dict_0):
        menu_lvl_1 = menu_dict_0[menu_id]
        menu_lvl_1['class'] = 'hide'
        for menu_lvl_2 in menu_lvl_1['subs']:
            menu_lvl_2['url'] = reverse(menu_lvl_2['name'])
            if menu_lvl_2['id'] == current_pid:
                menu_lvl_2['class'] = 'active'
                menu_lvl_1['class'] = ''
        menu_dict[menu_id] = menu_lvl_1
    print(menu_dict, 'in rbac inclusion_tag')
    return {'menu_dict': menu_dict}


@register.inclusion_tag('rbac/bread_crumb.html')
def bread_crumb(request):
    url_record = request.breadcrumb
    for item in url_record:
        try:
            item['url'] = reverse(item['name'])
        except NoReverseMatch:
            pass
    return {'url_record': url_record}


@register.filter
def has_permission(request, name):  # filter的第一个参数时过滤器前面的对象
    if name in request.session[settings.RBAC_PERMISSION_KEY]:
        return True

