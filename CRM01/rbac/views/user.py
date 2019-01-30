from django.shortcuts import HttpResponse,render,reverse,redirect
from rbac.models import *
from rbac.forms.user import UserEditForm,UserCreateForm,UserResetForm


def user_list(request):
    user_query_set = UserInfo.objects.all()
    return render(request,'rbac/user_list.html',{'users':user_query_set})


def user_add(request):
    if request.method == 'GET':
        form = UserCreateForm()
        return render(request, 'rbac/change.html', {'form': form})
    user = UserCreateForm(data=request.POST)
    if user.is_valid():
        user.save()
        return redirect(reverse('rbac:user_list'))
    else:
        return render(request, 'rbac/change.html', {'form': user})


def user_edit(request,user_id):
    user = UserInfo.objects.filter(id=user_id).first()
    if not user:
        return HttpResponse('该用户不存在')
    if request.method == 'GET':
        form = UserEditForm(instance=user)
        return render(request, 'rbac/change.html', {'form': form})
    user = UserEditForm(data=request.POST, instance=user)
    if user.is_valid():
        user.save()
        return redirect(reverse('rbac:user_list'))
    else:
        return render(request, 'rbac/change.html', {'form': user})


def user_del(request,user_id):
    user = UserInfo.objects.filter(id=user_id).first()
    if request.method == 'POST':
        user.delete()
        return redirect(reverse('rbac:user_list'))
    else:
        msg={'back': reverse('rbac:user_list'), 'item': user.name}
        return render(request, 'rbac/delete_warning.html', {'msg': msg})


def user_reset_password(request,user_id):
    user = UserInfo.objects.filter(id=user_id).first()
    if not user:
        return HttpResponse('该用户不存在')
    if request.method == 'GET':
        form = UserResetForm(instance=user)
        return render(request, 'rbac/change.html', {'form': form})
    user = UserResetForm(data=request.POST, instance=user)
    if user.is_valid():
        user.save()
        return redirect(reverse('rbac:user_list'))
    else:
        return render(request, 'rbac/change.html', {'form': user})