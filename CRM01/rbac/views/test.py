from django.shortcuts import render
from rbac.service.my_tools import find_all_urls

def test(requests):
    find_all_urls()
    return render(requests,'rbac/test.html')