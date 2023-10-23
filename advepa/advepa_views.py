from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='advepa:login')
def index(request):
    if request.user.role == 'administrator' or request.user.role == 'standist':
        return redirect('advepa:actions')
    else:
        return redirect('advepa:dashboard')


def page_error_400(request, *args, **argv):
    return render(request, '400.html')


def page_error_403(request, *args, **argv):
    return render(request, '403.html')


def page_error_404(request, *args, **argv):
    return render(request, '404.html')


def page_error_500(request, *args, **argv):
    return render(request, '500.html')


def page_error_503(request, *args, **argv):
    return render(request, '503.html')
