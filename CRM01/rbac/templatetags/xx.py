#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   xx.py
@Time    :   2019/1/29 12:59
@Desc    :
'''
from django.template import Library

register = Library()  # 一定要写成register


@register.simple_tag
def xxx():
    return '123456789'

