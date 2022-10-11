from django.contrib.auth import authenticate, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_user
from django.shortcuts import redirect, reverse, render
from django.http import HttpResponseNotAllowed


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_user(request, user)
            return redirect(reverse('account'))
        return render(request, 'login_data_invalid.html')
    return HttpResponseNotAllowed()


@login_required
def logout(request):
    logout_user(request)
    return redirect(reverse('home'))

