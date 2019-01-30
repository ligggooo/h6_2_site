#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   test.py
@Time    :   2019/1/28 17:42
@Desc    :
'''
from django.shortcuts import HttpResponse

def test(request):
    return HttpResponse('web testing...')