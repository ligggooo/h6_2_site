from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count,F
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

import json
import time
import os
from  h6_2_site import settings
from blog.models import *
from .utils import capcha as cap
from .utils import security
# 基于form表单的用户注册模块
from blog.myform import UserForm

# Create your views here.


# @login_required
def index(request):
    page_num = request.GET.get('page',1)
    user = request.user
    articles = Article.objects.all().order_by('create_time').reverse()
    # 分页器
    paginator = Paginator(articles, 10)
    page = request.GET.get('page', 1)
    currentPage = int(page)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    res = HttpResponse('你所在的区域不能访问该资源')
    res.status_code = '403'
    # return render(request, 'blog/index.html', locals())
    return res

def login(request):
    next_page = request.GET.get('next', '/index/')
    if request.method == 'POST':
        response = {'msg': None, 'user': None, 'next': next_page}
        user_name = request.POST.get('username')
        pass_word = request.POST.get('passwd')
        cap_code = request.POST.get('cap_code')
        valid_cap_code = request.session.get('cap_code')
        print(cap_code, valid_cap_code)
        if cap_code.upper() == valid_cap_code.upper():# root 1234
            user = auth.authenticate(username=user_name, password=pass_word)
            if not user:
                response['msg'] = '账户或者密码错误'
            else:
                auth.login(request, user)
                response['user'] = user_name
                response['msg'] = 'success'  # 前端收到这个就可以跳转了
        else:
            response['msg'] = '验证码错误'
        return JsonResponse(response)
    return render(request, 'blog/login.html', locals())

def logout(request):
    user=request.user
    auth.logout(request)
    return redirect('/index/')

def capcha(request):
    capcha_bytes,cap_code = cap.getcapcha()
    request.session['cap_code'] = cap_code
    return HttpResponse(capcha_bytes)




def register(request):
    form = UserForm(request.POST) # 构建表单对象
    # print(form)
    if request.is_ajax():
        response = {'msg': None, 'user': None, 'next': '/login/'}
        if form.is_valid():
            response['msg'] = 'success'
            response['user'] = form.cleaned_data.get('user')
            user = form.cleaned_data.get('user')
            pwd = form.cleaned_data.get('pwd')
            email = form.cleaned_data.get('email')
            avatar_obj = request.FILES.get('avatar')
            if avatar_obj:  # 防止用户上传空文件，那样会在这个字段会有一个None，与默认是两码事
                UserInfo.objects.create_user(username=user,password=pwd,email=email,avatar=avatar_obj)
            else:
                UserInfo.objects.create_user(username=user, password=pwd, email=email)
        else:
            print(form.cleaned_data)
            print(form.errors)
            response['msg']=form.errors
        return JsonResponse(response)
    return render(request, 'blog/register.html', locals())

# @login_required
def user_site(request,username,type=None,params=None):
    '''
    个人站点
    :param request:
    :param username:
    :return:
    '''
    user = UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, 'error404.html')
    else:
        # 写上一堆查询
        blog = user.blog
        # 该作者的文章
        articles = Article.objects.filter(user=user)
        # 每个分类的id,所属的文章数目
        # categories = Category.objects.filter(blog=blog)
        categories = Article.objects.filter(user=user).values_list('category__nid', 'category__title').annotate(c=Count('title'))
        # 每个标签下的文章数量
        tags = Tag.objects.filter(blog=blog).values('nid','title').annotate(c=Count('article__nid'))
        # 日期分组
        date_records = Article.objects.filter(user=user)\
            .extra(select={'d': "strftime('%%Y-%%m-%%d',create_time)"})\
            .values('d').annotate(c=Count('nid'))

        # 根据 条件 过滤 articles
        from django.db.models.functions import TruncDate
        if params and type:
            if type=='cate':
                if params=='none':
                    articles = articles.filter(category__nid=None)
                    main_title_2 = '未分类'
                else:
                    articles = articles.filter(category__nid=params)
                    main_title_2 = Category.objects.get(nid=params).title
                main_title_1 = '分类'

            elif type=='tag':
                main_title_1 = '标签'
                main_title_2 = Tag.objects.get(nid=params).title
                articles = articles.filter(tags__nid=params).distinct()
            elif type=='date':
                main_title_1 = '日期'
                main_title_2 = params
                year,month,day = params.split('-')
                articles = articles.filter(create_time__year=year,create_time__month=month,create_time__day=day)
        else:
                # main_title_1 = '全部'
                pass
        return render(request, 'blog/user_site.html', locals())

def article_detail(request,username,article_id):
    user = UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, 'error404.html')
    else:
        # 写上一堆查询
        blog = user.blog
        # 该作者的文章
        articles = Article.objects.filter(user=user)
        # 每个分类的id,所属的文章数目
        # categories = Category.objects.filter(blog=blog)
        categories = Article.objects.filter(user=user).values_list('category__nid', 'category__title').annotate(c=Count('title'))
        # 每个标签下的文章数量
        tags = Tag.objects.filter(blog=blog).values('nid','title').annotate(c=Count('article__nid'))
        # 日期分组
        date_records = Article.objects.filter(user=user)\
            .extra(select={'d': "strftime('%%Y-%%m-%%d',create_time)"})\
            .values('d').annotate(c=Count('nid'))

        article = Article.objects.filter(nid=article_id,user=user).first()
        if not article:
            return render(request, 'error404.html')

        comments = Comment.objects. \
            filter(article=article, parent_comment=None).values_list('nid', 'user__nid',
                                                    'user__username', 'content', 'create_time', 'parent_comment__nid')
        return render(request,'blog/article_detail.html',locals())


def article_up_down(request):
    action_user = request.user
    response = {'msg':None,'code':None}
    if not action_user.is_authenticated:
        response['msg'] = '请先'
        response['code'] = 1  # 登陆
    else:
        article_id = request.POST.get('article_id')
        article = Article.objects.filter(nid=article_id).first()
        if not article:
            response['msg'] = '找不到该文章'
            response['code'] = 2  #
        else:
            is_up = json.loads(request.POST.get('is_up'))
            up_obj = ArticleUpDown.objects.filter(article=article, user=action_user).first()
            if not up_obj:
                ArticleUpDown.objects.create(article=article, user=action_user, is_up=is_up)
                if is_up:
                    Article.objects.filter(nid=article_id).update(up_count=F('up_count')+1)
                else:
                    Article.objects.filter(nid=article_id).update(down_count=F('down_count') + 1)
                response['msg'] = is_up
                response['code'] = 0  #
            elif up_obj.is_up == is_up:
                response['msg'] = '不能重复赞或踩'
                response['code'] = 3  #
            elif up_obj.is_up != is_up:   # 赞踩切换
                ArticleUpDown.objects.filter(article=article, user=action_user).update(is_up=is_up)
                if is_up:   # 踩变赞
                    Article.objects.filter(nid=article_id).update(up_count=F('up_count') + 1,
                                                                  down_count=F('down_count')-1)
                else:
                    Article.objects.filter(nid=article_id).update(up_count=F('up_count') - 1,
                                                                  down_count=F('down_count') + 1)
                response['msg'] = is_up
                response['code'] = 4  # 切换
    return JsonResponse(response)

def comment(request):
    response={'msg':None,'status':None}
    action_user = request.user
    target = request.POST.get('target')
    article_obj = Article.objects.get(nid=request.POST.get('article_id'))
    content = request.POST.get('content')
    if not article_obj:
        response['msg'] = '无此文章'
        response['status'] = 1
    else:
        if target.isdigit():
            parent_comment = Comment.objects.filter(nid = target).first()
            if not parent_comment:
                response['msg'] = '无此评论'
                response['status'] = 1
            else:
                Comment.objects.create(user=action_user,article=article_obj,content=content,parent_comment=parent_comment)
                response['msg'] = '成功创建子评论'
                response['status'] = 0
        else:
            Comment.objects.create(user=action_user, article=article_obj, content=content)
            response['msg'] = '成功创建根评论'
            response['status'] = 0
            # 创建跟评论 ， 文章评论数加1
            Article.objects.filter(nid=request.POST.get('article_id')).update(comment_count=F('comment_count')+1)
    return JsonResponse(response)

def get_comments(request):
    response = {'msg': None, 'status': None}
    article_obj = Article.objects.get(nid=request.POST.get('article_id'))
    if not article_obj:
        response['msg'] = '无此文章'
        response['status'] = 1
    else:
        comments = Comment.objects.\
            filter(article=article_obj).values('nid', 'user__nid',
                                               'user__username','content','create_time', 'parent_comment__nid')
        for c in comments:
            c['create_time'] = c['create_time'].strftime('%Y-%m-%d %H:%M:%S')
        response['msg'] = list(comments)
        response['status'] = 0
    return JsonResponse(response)


@login_required
def backend(request):
    articles = Article.objects.filter(user=request.user)
    return render(request,'blog/backend.html',locals())

@login_required
def backend_add_article(request):
    if request.method=='POST':
        response = {'msg': None, 'status': None}
        text,desc = security.clear_text(request.POST.get('article_content'))
        title = request.POST.get('title')
        user = request.user
        print(title,text)
        Article.objects.create(title=title,content=text,user=user,desc=desc)
        response['msg']='success'
        response['status'] = 0
        return JsonResponse(response)
    return render(request, 'blog/backend_add.html', locals())


@login_required
def backend_edit_article(request,article_id):
    user = request.user
    article_obj = Article.objects.filter(nid=article_id,user=user).first()
    if not article_obj:
        return HttpResponse('文章不存在')
    else:
        if request.method == 'POST':
            response = {'msg': None, 'status': None}
            text, desc = security.clear_text(request.POST.get('article_content'))
            title = request.POST.get('title')
            user = request.user
            Article.objects.filter(nid=article_id,user=user).update(title=title, content=text, user=user, desc=desc)
            response['msg'] = 'success'
            response['status'] = 0
            return JsonResponse(response)
        else:
            return render(request, 'blog/backend_edit.html', locals())

@login_required
def backend_rm_article(request):  # ajax 操作
    article_id = request.POST.get('target')
    response = {'msg': None, 'status': None}
    user = request.user
    article_obj=Article.objects.filter(nid=article_id,user=user).first()
    if not article_obj:
        response['msg']='目标不存在或无权删除'
        response['status']=1
    else:
        title = article_obj.title
        Article.objects.filter(nid=article_id, user=user).delete()
        response['msg'] = '成功删除《%s》'%title
        response['status'] = 0
    return JsonResponse(response)

def upload(request):
    print(request.FILES)
    file= request.FILES.get('imgFile')
    filename = str(round(time.time()))+file.name
    with open(os.path.join(settings.MEDIA_ROOT,'upload_img/')+filename,'wb') as f:
        for line in file:
            f.write(line)
    url = '/media/upload_img/'+filename
    response = {
        "error":0,
        "url":url
    }
    return JsonResponse(response)