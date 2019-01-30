from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=32,unique=True,verbose_name='菜单标题')
    icon = models.CharField(max_length=32,verbose_name='菜单图标')

    def __str__(self):
        return self.title


class Permission(models.Model):
    title = models.CharField(max_length=32,unique=True,verbose_name='权限标题')
    url = models.CharField(max_length=128,verbose_name='url正则表达式')
    name = models.CharField(max_length=32,unique=True,verbose_name='别名',help_text='与url别名相同，可用于反向解析')
    menu = models.ForeignKey(to='Menu',to_field='id',null=True,blank=True,on_delete=models.PROTECT,
                             verbose_name='所属菜单',help_text='null 表示不属于任何菜单，否则属于一个菜单')
    pid = models.ForeignKey(to='self',related_name='parent',null=True,blank=True,verbose_name='关联权限',
                            help_text='例如：用户删除权限不能做菜单，但是点击这个选项，会使得用户列表这个菜单处于被激活状态',
                            on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='Role', blank=True)

    def __str__(self):
        return self.name

