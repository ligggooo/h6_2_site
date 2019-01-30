from django.shortcuts import render

def test(requests):
    return render(requests,'rbac/test.html')