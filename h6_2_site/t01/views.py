from django.shortcuts import render

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
