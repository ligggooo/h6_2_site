from django.shortcuts import render,HttpResponse
from blog.models import *
from django.db.models import F,Q

# Create your views here.

def book(requests):
    books = [{
        'name':'JavaScript+DOM编程艺术',
        'filename':'JavaScript+DOM编程艺术（清晰中文版） - 副本.pdf',
    },{
        'name': 'JavaScript高级程序设计（第3版）',
        'filename':'JavaScript高级程序设计（第3版）非扫描版 - 副本.pdf',

    }]
    return render(requests, 'fun/books.html', locals())

def index(request):
    return render(request,'t01/index2.html')

def test_view(request):
    article_obj = Article.objects.filter(user__username='lee').first()
    print(article_obj)
    cates = Category.objects.filter(blog__userinfo__username='lee').all()
    print(cates)
    # category = models.ForeignKey(to='Category', to_field='nid',
    #                              limit_choices_to=models.Q(blog_id=models.F('blog_id')),  # 不起作用
    #                              # limit_choices_to=models.Q(blog_id=1),  # 起作用
    #                              null=True, on_delete=models.CASCADE)
    return HttpResponse('ok')
