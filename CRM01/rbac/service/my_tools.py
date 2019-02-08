#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   my_tools.py
@Time    :   2019/1/29 21:19
@Desc    :
'''


def bypass(func):
    def bypassed_func(*args,**kwargs):
        # z= func(*args,**kwargs)
        print('func %s is bypassed for testing...'%func)
        return None
    return bypassed_func


from collections import OrderedDict
from django.urls import URLResolver,URLPattern

def get_all(patterns,ans):
    for item in patterns:
        if isinstance(item, URLResolver):
            print('yes', item.namespace,item.pattern)
            get_all(item.url_patterns,ans)
        elif isinstance(item, URLPattern):
            print('no', item.name)
        else:
            print('?????????????',item.name)



def find_all_urls():
    ans = []# OrderedDict()
    from django.conf import settings

    # print(settings.ROOT_URLCONF)
    a= __import__(settings.ROOT_URLCONF)
    get_all(a.urls.urlpatterns,ans)


# if __name__=='__main__':
#     find_all_urls()