#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   myform.py
@Time    :   2019/1/17 16:34
@Desc    :
'''
from django import forms
from django.forms import widgets  # 快速定义form字段
from blog.models import UserInfo
from django.core.exceptions import ValidationError

w_text = widgets.TextInput(attrs={'class': 'form-control'})
w_pwd = widgets.PasswordInput(attrs={'class': 'form-control'},)
w_email = widgets.EmailInput(attrs={'class': 'form-control'},)


class UserForm(forms.Form):
    user = forms.CharField(max_length=32,error_messages={'required':'此字段不能为空'},
                           empty_value='输入用户名',widget=w_text,label='用户名')
    pwd = forms.CharField(max_length=32,error_messages={'required':'此字段不能为空'},
                          empty_value='输入密码',widget=w_pwd,label='密码')
    re_pwd = forms.CharField(max_length=32,error_messages={'required':'此字段不能为空'},
                             empty_value='再次输入密码',widget=w_pwd,label='确认密码')
    email = forms.EmailField(max_length=32,error_messages={'required': '此字段不能为空',
                                                           'invalid': '请输入有效的邮箱地址'},
                             empty_value='输入邮箱',widget=w_text,label='邮箱')

    def clean_user(self):
        val = self.cleaned_data.get("user")
        record = UserInfo.objects.filter(username=val).first()
        if not record:
            return val
        else:
            raise ValidationError("该用户已经注册")

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd == re_pwd or not (pwd and re_pwd):
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致')
