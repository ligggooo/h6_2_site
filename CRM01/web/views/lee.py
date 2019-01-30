#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   lee.py
@Time    :   2019/1/24 21:29
@Desc    :
'''
from django.http import HttpResponse
from django.shortcuts import redirect
import time


def index(request):
    print(request.session.get('haha', 'N/A'))
    time.sleep(2)
    request.session['haha'] = time.ctime()
    # return HttpResponse('ok')

    return redirect('http://www.baidu.com')

