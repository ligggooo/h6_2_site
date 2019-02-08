#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   url_search.py
@Time    :   2019/2/1 9:46
@Desc    :
'''
from collections import OrderedDict
from django.urls import URLResolver,URLPattern


def get_all(pre_root, pre_namespace, patterns, ans):
    for item in patterns:
        if isinstance(item, URLResolver):
            # print('分发 --', item.namespace,item.pattern)
            if item.namespace and pre_namespace:
                namespace = pre_namespace+':'+item.namespace
            elif not pre_namespace and item.namespace:
                namespace = item.namespace
            elif pre_namespace and not item.namespace:
                namespace = pre_namespace
            else:
                namespace = None
            # try:
            #     root = root + item.pattern._route
            # except AttributeError as e:
            #     print(e)
            root = pre_root + str(item.pattern).replace('^', '').replace('$', '')
            # print('分发 --', namespace, root)
            get_all(root,namespace,item.url_patterns,ans)

        elif isinstance(item, URLPattern):
            if not item.name:
                continue
            if item.name and pre_namespace:
                name = pre_namespace+':'+item.name
            else:
                name = item.name
            pattern = pre_root + str(item.pattern).replace('^','').replace('$','')
            ans[name] = pattern
            # print('    匹配 ----',name,pattern)
        else:
            # print('?????????????',item.name)
            pass


def find_all_urls():
    ans = OrderedDict()
    from django.conf import settings

    # print(settings.ROOT_URLCONF)
    a= __import__(settings.ROOT_URLCONF)
    get_all('/',None, a.urls.urlpatterns, ans=ans)
    return ans


if __name__=='__main__':
    print('------------------------------')
    xx = find_all_urls()
    for x in xx:
        print(xx)