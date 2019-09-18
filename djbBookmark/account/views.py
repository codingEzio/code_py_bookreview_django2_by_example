from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .forms import LoginForm


def user_login(request):
    """The differences
    ~ authenticate    check whether the name/pwd is right
    ~ login           sets you in the session (aka. logged in)
    """

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('驗證成功!')

                else:
                    return HttpResponse('此賬戶已被禁用 :(')

            else:
                return HttpResponse('非法登入 (錯誤的用戶名或密碼).')

    else:
        form = LoginForm()

    return render(request,
                  'account/login.html',
                  { 'form': form })
