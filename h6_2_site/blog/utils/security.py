#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   security.py
@Time    :   2019/1/20 22:22
@Desc    :
'''
from bs4 import BeautifulSoup

def clear_text(text):
    soup = BeautifulSoup(text,'html.parser')
    print(soup.text)
    desc = soup.text[:150]
    for tag in soup.find_all():
        if tag.name in ['script','style','link']:
            tag.decompose()
    return text,desc
