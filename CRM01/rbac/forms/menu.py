#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   menu.py
@Time    :   2019/1/30 19:40
@Desc    :
'''
from django.forms import ModelForm,Form,ValidationError,TextInput,\
    RadioSelect,Select,CharField,ChoiceField,HiddenInput,IntegerField
from rbac.models import Menu,Permission
from django.utils.safestring import mark_safe

ICON_LIST = [
    ['fa-address-book', '<i class="fa fa-address-book" aria-hidden="true"></i>'],
    ['fa-address-book-o', '<i class="fa fa-address-book-o" aria-hidden="true"></i>'],
    ['fa-address-card', '<i class="fa fa-address-card" aria-hidden="true"></i>'],
    ['fa-address-card-o', '<i class="fa fa-address-card-o" aria-hidden="true"></i>'],
    ['fa-adjust', '<i class="fa fa-adjust" aria-hidden="true"></i>'],
    ['fa-american-sign-language-interpreting',
     '<i class="fa fa-american-sign-language-interpreting" aria-hidden="true"></i>'],
    ['fa-anchor', '<i class="fa fa-anchor" aria-hidden="true"></i>'],
    ['fa-archive', '<i class="fa fa-archive" aria-hidden="true"></i>'],
    ['fa-area-chart', '<i class="fa fa-area-chart" aria-hidden="true"></i>'],
    ['fa-arrows', '<i class="fa fa-arrows" aria-hidden="true"></i>'],
    ['fa-arrows-h', '<i class="fa fa-arrows-h" aria-hidden="true"></i>'],
    ['fa-arrows-v', '<i class="fa fa-arrows-v" aria-hidden="true"></i>'],
    ['fa-asl-interpreting', '<i class="fa fa-asl-interpreting" aria-hidden="true"></i>'],
    ['fa-assistive-listening-systems', '<i class="fa fa-assistive-listening-systems" aria-hidden="true"></i>'],
    ['fa-asterisk', '<i class="fa fa-asterisk" aria-hidden="true"></i>'],
    ['fa-at', '<i class="fa fa-at" aria-hidden="true"></i>'],
    ['fa-audio-description', '<i class="fa fa-audio-description" aria-hidden="true"></i>'],
    ['fa-automobile', '<i class="fa fa-automobile" aria-hidden="true"></i>'],
    ['fa-balance-scale', '<i class="fa fa-balance-scale" aria-hidden="true"></i>'],
    ['fa-ban', '<i class="fa fa-ban" aria-hidden="true"></i>'],
    ['fa-bank', '<i class="fa fa-bank" aria-hidden="true"></i>'],
    ['fa-bar-chart', '<i class="fa fa-bar-chart" aria-hidden="true"></i>'],
    ['fa-bar-chart-o', '<i class="fa fa-bar-chart-o" aria-hidden="true"></i>'],
    ['fa-barcode', '<i class="fa fa-barcode" aria-hidden="true"></i>'],
    ['fa-bars', '<i class="fa fa-bars" aria-hidden="true"></i>'],
    ['fa-bath', '<i class="fa fa-bath" aria-hidden="true"></i>'],
    ['fa-bathtub', '<i class="fa fa-bathtub" aria-hidden="true"></i>'],
    ['fa-battery', '<i class="fa fa-battery" aria-hidden="true"></i>'],
    ['fa-battery-0', '<i class="fa fa-battery-0" aria-hidden="true"></i>'],
    ['fa-battery-1', '<i class="fa fa-battery-1" aria-hidden="true"></i>'],
    ['fa-battery-2', '<i class="fa fa-battery-2" aria-hidden="true"></i>'],
    ['fa-battery-3', '<i class="fa fa-battery-3" aria-hidden="true"></i>'],
    ['fa-battery-4', '<i class="fa fa-battery-4" aria-hidden="true"></i>'],
    ['fa-battery-empty', '<i class="fa fa-battery-empty" aria-hidden="true"></i>'],
    ['fa-battery-full', '<i class="fa fa-battery-full" aria-hidden="true"></i>'],
    ['fa-battery-half', '<i class="fa fa-battery-half" aria-hidden="true"></i>'],
    ['fa-battery-quarter', '<i class="fa fa-battery-quarter" aria-hidden="true"></i>'],
    ['fa-battery-three-quarters', '<i class="fa fa-battery-three-quarters" aria-hidden="true"></i>'],
    ['fa-bed', '<i class="fa fa-bed" aria-hidden="true"></i>'],
    ['fa-beer', '<i class="fa fa-beer" aria-hidden="true"></i>'],
    ['fa-bell', '<i class="fa fa-bell" aria-hidden="true"></i>'],
    ['fa-bell-o', '<i class="fa fa-bell-o" aria-hidden="true"></i>'],
    ['fa-bell-slash', '<i class="fa fa-bell-slash" aria-hidden="true"></i>'],
    ['fa-bell-slash-o', '<i class="fa fa-bell-slash-o" aria-hidden="true"></i>'],
    ['fa-bicycle', '<i class="fa fa-bicycle" aria-hidden="true"></i>'],
    ['fa-binoculars', '<i class="fa fa-binoculars" aria-hidden="true"></i>'],
    ['fa-birthday-cake', '<i class="fa fa-birthday-cake" aria-hidden="true"></i>'],
    ['fa-blind', '<i class="fa fa-blind" aria-hidden="true"></i>'],
    ['fa-bluetooth', '<i class="fa fa-bluetooth" aria-hidden="true"></i>'],
    ['fa-bluetooth-b', '<i class="fa fa-bluetooth-b" aria-hidden="true"></i>'],
    ['fa-bolt', '<i class="fa fa-bolt" aria-hidden="true"></i>'],
    ['fa-bomb', '<i class="fa fa-bomb" aria-hidden="true"></i>'],
    ['fa-book', '<i class="fa fa-book" aria-hidden="true"></i>'],
    ['fa-bookmark', '<i class="fa fa-bookmark" aria-hidden="true"></i>'],
    ['fa-bookmark-o', '<i class="fa fa-bookmark-o" aria-hidden="true"></i>'],
    ['fa-braille', '<i class="fa fa-braille" aria-hidden="true"></i>'],
    ['fa-briefcase', '<i class="fa fa-briefcase" aria-hidden="true"></i>'],
    ['fa-bug', '<i class="fa fa-bug" aria-hidden="true"></i>'],
    ['fa-building', '<i class="fa fa-building" aria-hidden="true"></i>'],
    ['fa-building-o', '<i class="fa fa-building-o" aria-hidden="true"></i>'],
    ['fa-bullhorn', '<i class="fa fa-bullhorn" aria-hidden="true"></i>'],
    ['fa-bullseye', '<i class="fa fa-bullseye" aria-hidden="true"></i>'],
    ['fa-bus', '<i class="fa fa-bus" aria-hidden="true"></i>'],
    ['fa-cab', '<i class="fa fa-cab" aria-hidden="true"></i>'],
    ['fa-calculator', '<i class="fa fa-calculator" aria-hidden="true"></i>'],
    ['fa-calendar', '<i class="fa fa-calendar" aria-hidden="true"></i>'],
    ['fa-calendar-check-o', '<i class="fa fa-calendar-check-o" aria-hidden="true"></i>'],
    ['fa-calendar-minus-o', '<i class="fa fa-calendar-minus-o" aria-hidden="true"></i>'],
    ['fa-calendar-o', '<i class="fa fa-calendar-o" aria-hidden="true"></i>'],
    ['fa-calendar-plus-o', '<i class="fa fa-calendar-plus-o" aria-hidden="true"></i>'],
    ['fa-calendar-times-o', '<i class="fa fa-calendar-times-o" aria-hidden="true"></i>'],
    ['fa-camera', '<i class="fa fa-camera" aria-hidden="true"></i>'],
    ['fa-camera-retro', '<i class="fa fa-camera-retro" aria-hidden="true"></i>'],
    ['fa-car', '<i class="fa fa-car" aria-hidden="true"></i>'],
    ['fa-caret-square-o-down', '<i class="fa fa-caret-square-o-down" aria-hidden="true"></i>'],
    ['fa-caret-square-o-left', '<i class="fa fa-caret-square-o-left" aria-hidden="true"></i>'],
    ['fa-caret-square-o-right', '<i class="fa fa-caret-square-o-right" aria-hidden="true"></i>'],
    ['fa-caret-square-o-up', '<i class="fa fa-caret-square-o-up" aria-hidden="true"></i>'],
    ['fa-cart-arrow-down', '<i class="fa fa-cart-arrow-down" aria-hidden="true"></i>'],
    ['fa-cart-plus', '<i class="fa fa-cart-plus" aria-hidden="true"></i>'],
]
ICON_LIST = list(map(lambda x:[x[0], mark_safe(x[1])],ICON_LIST))

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ['title', 'icon']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'icon': RadioSelect(choices=ICON_LIST, attrs={'class': 'clearfix icon_select'})
        }

class SecondMenuForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        # menus = Menu.objects.values_list('id', 'title')
        # self.fields['menu'] = Select(choices=menus, attrs={'class': 'form-control'})

    class Meta:
        model = Permission
        fields = ['title', 'url', 'name', 'menu']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'url': TextInput(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'menu': Select(attrs={'class': 'form-control'})
        }


class PermissionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # parents = Permission.objects.filter(menu_id__isnull=False).values_list('id','title')
        # self.fields['pid'].widget = Select(choices=parents, attrs={'class': 'form-control'})

    class Meta:
        model = Permission
        fields = ['title', 'url', 'name']#, 'pid']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'url': TextInput(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            # 'pid': Select(attrs={'class': 'form-control'})
        }

class MultiAddPermissionForm(Form):
    title = CharField(
        widget=TextInput(attrs={'class': "form-control"})
    )
    url = CharField(
        widget=TextInput(attrs={'class': "form-control"})
    )
    name = CharField(
        widget=TextInput(attrs={'class': "form-control"})
    )
    menu_id = ChoiceField(
        choices=[(None, '-----')],
        widget=Select(attrs={'class': "form-control"}),
        required=False,

    )
    pid_id = ChoiceField(
        choices=[(None, '-----')],
        widget=Select(attrs={'class': "form-control"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')


class MultiAddPermissionUpdateForm(Form):
    id = IntegerField(widget=HiddenInput(),label='序列号')   # 编辑表单多了一个隐藏的id字段
    title = CharField(
        widget=TextInput(attrs={'class': "form-control"}),label='标题'
    )
    url = CharField(
        widget=TextInput(attrs={'class': "form-control"}),label='url'
    )
    name = CharField(
        widget=TextInput(attrs={'class': "form-control"}),label='名称'
    )
    menu_id = ChoiceField(
        choices=[(None, '-----')],
        widget=Select(attrs={'class': "form-control"}),
        required=False,label='属菜单'
    )
    pid_id = ChoiceField(
        choices=[(None, '-----')],
        widget=Select(attrs={'class': "form-control"}),
        required=False,label='关联权限'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')

