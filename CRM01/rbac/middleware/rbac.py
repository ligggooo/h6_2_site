#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   rbac_middleware.py
@Time    :   2019/1/28 17:33
@Desc    :
'''

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings
import re


class RBACMiddleware(MiddlewareMixin):

    from rbac.service.my_tools import bypass

    @bypass
    def process_request(self, request):
        current_path = request.path_info[1:]
        white_list = settings.URL_WHITE_LIST
        for pattern in white_list:
            if re.match(pattern, current_path):
                return None

        permissions = request.session.get(settings.RBAC_PERMISSION_KEY)

        url_record = [
            {'title': '首页', 'name': settings.INDEX_NAME}
        ]

        if not permissions:
            return HttpResponse('No access for an anonymous user.Please login first.')
        for permission in permissions.values():
            # 实现了权限控制，但是还没实现分级菜单和导航条
            pattern = permission['url']

            if re.match(pattern, current_path):
                request.current_selected_permission_id = permission['parent_id'] or permission['id']
                if not permission['parent_id']:
                    url_record.extend([{'title': permission['title'], 'name': permission['name'], 'class': 'active'}])
                else:
                    url_record.extend([
                        {'title': permission['parent_title'], 'name': permission['parent_name']},
                        {'title': permission['title'], 'name': permission['name'], 'class': 'active'},
                    ])
                request.breadcrumb = url_record
                return None
        return HttpResponse('No access.')



