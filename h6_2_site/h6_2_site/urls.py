"""h6_2_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.views.static import serve
import blog.views
from h6_2_site import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', blog.views.index),
    path('login/', blog.views.login),
    path('logout/', blog.views.logout),
    path('register/', blog.views.register),
    path('cap/', blog.views.capcha),
    path('backend/',blog.views.backend),

    path('backend/add_article/',blog.views.backend_add_article),
    re_path(r'^backend/edit_article/(?P<article_id>\d*)$',blog.views.backend_edit_article),
    path('backend/remove_article/', blog.views.backend_rm_article),

    path('upload/',blog.views.upload),
    path('dig_up/', blog.views.article_up_down),
    path('comment/', blog.views.comment), # ajax 访问路径
    path('get_comments/', blog.views.get_comments), # ajax 访问路径

    re_path('^$', blog.views.index),
    re_path('^(?P<username>\w+)/(?P<type>cate|tag|date)/(?P<params>.*)$', blog.views.user_site),
    re_path('^(?P<username>\w+)/articles/(?P<article_id>\d*)$', blog.views.article_detail),

    re_path('^(?P<username>\w+)$', blog.views.user_site),

    #     配置media文件路径
    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT})
]
