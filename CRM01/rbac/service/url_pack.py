#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   url_pack.py
@Time    :   2019/1/31 16:25
@Desc    :
'''
from django.http import QueryDict
from django.shortcuts import reverse

def url_param_pack(request, name,*args,**kwargs):
    url = reverse(name, args=args, kwargs=kwargs)
    params = QueryDict(mutable=True)
    if not request.GET:
        return url
    params_pack = request.GET.urlencode()
    params['_anchor'] = params_pack
    return url + '?' + params.urlencode()


def url_param_unpack(request, target_name, *args,**kwargs):
    param_pack = request.GET.get('_anchor')
    target_url = reverse(target_name,args=args,kwargs=kwargs)
    if not param_pack:
        return target_url
    return target_url+'?'+param_pack

# def url_param_unpack_get(request):
#     from urllib import unquote
#     param_pack = request.GET.get('_anchor')
#     if not param_pack:
#         return None
#     return param_pack.


