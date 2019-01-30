#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   urls.py
@Time    :   2019/1/28 16:10
@Desc    :
'''

from django.urls import path,include,re_path
from rbac.views.test import test
from rbac.views import role,user,menu

app_name = 'rbac'
urlpatterns = [
    re_path('^test/$', test,name='test'),

    re_path('^role/list/$',role.role_list, name='role_list'),
    re_path('^role/add/$',role.role_add, name='role_add'),
    re_path('^role/edit/(?P<role_id>\d+)/$', role.role_edit, name='role_edit'),
    re_path('^role/del/(?P<role_id>\d+)/$', role.role_del, name='role_del'),

    re_path('^user/list/$', user.user_list, name='user_list'),
    re_path('^user/add/$', user.user_add, name='user_add'),
    re_path('^user/edit/(?P<user_id>\d+)/$', user.user_edit, name='user_edit'),
    re_path('^user/del/(?P<user_id>\d+)/$', user.user_del, name='user_del'),
    re_path('^user/reset/(?P<user_id>\d+)/$', user.user_reset_password, name='user_reset_password'),

    re_path(r'^menu/list/$', menu.menu_list, name='menu_list'),
    re_path(r'^menu/add/$', menu.menu_add, name='menu_add'),
    re_path(r'^menu/edit/(?P<menu_id>\d+)/$', menu.menu_edit, name='menu_edit'),
    re_path(r'^menu/del/(?P<menu_id>\d+)/$', menu.menu_del, name='menu_del'),

    re_path(r'^multi/permissions/$', menu.multi_permissions, name='multi_permissions'),
]

