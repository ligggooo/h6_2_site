#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   role.py
@Time    :   2019/1/30 12:09
@Desc    :
'''
from django.forms import ModelForm,ValidationError,TextInput
from rbac.models import Role

class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['title']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'})
        }

    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if Role.objects.filter(title=title).exists():
    #         raise ValidationError("此角色已经存在！")
    #     else:
    #         return title


