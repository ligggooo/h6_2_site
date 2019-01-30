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



if __name__=='__main__':

    @bypass
    def zz(sadas):
        print(sadas)

    zz()