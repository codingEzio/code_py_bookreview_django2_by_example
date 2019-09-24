from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from common.decorators import ajax_required
from .models import Profile, Contact
from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
)


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  { 'section': 'dashboard' })


def register(request):
    if request.method == 'POST':
        user_from = UserRegistrationForm(request.POST)

        if user_from.is_valid():
            new_user = user_from.save(commit=False)
            new_user.set_password(user_from.cleaned_data['password'])
            new_user.save()

            Profile.objects.create(user=new_user)

            return render(request,
                          'account/register_done.html',
                          { 'new_user': new_user, })

    else:
        user_from = UserRegistrationForm()

    return render(request,
                  'account/register.html',
                  { 'user_form': user_from, })


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


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'account/edit_profile.html',
                  { 'user_form'   : user_form,
                    'profile_form': profile_form })


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  { 'section': 'people',
                    'users'  : users })


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  { 'section': 'people',
                    'user'   : user })


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)

            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({ 'status': 'ok' })

        except User.DoesNotExist:
            return JsonResponse({ 'status': 'ko' })

    return JsonResponse({ 'status': 'ko' })
