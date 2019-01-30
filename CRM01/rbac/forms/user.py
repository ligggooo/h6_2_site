#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   user.py
@Time    :   2019/1/30 16:56
@Desc    :
'''
from django.forms import ModelForm,ValidationError,TextInput,CharField,PasswordInput,EmailInput
from rbac.models import UserInfo


class UserCreateForm(ModelForm):
    re_pwd = CharField(max_length=64, label='确认密码',widget=PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserInfo
        fields = ['name','email', 'password',  're_pwd']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'password': PasswordInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_re_pwd(self):
        password = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_pwd')
        if password == re_pwd:
            return re_pwd
        else:
            raise ValidationError('两次输入的密码不一致')


class UserEditForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['name', 'email']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
        }


class UserResetForm(ModelForm):
    re_pwd = CharField(max_length=64, label='确认密码', widget=PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserInfo
        fields = ['password', 're_pwd']
        widgets = {
            'password': PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_re_pwd(self):
        password = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_pwd')
        if password == re_pwd:
            return re_pwd
        else:
            raise ValidationError('两次输入的密码不一致')