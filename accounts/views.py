from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, authenticate, login, logout

from .models import UserProfile
from .forms import UserForm, UserProfileForm, UserLoginForm, UserEditForm, UserProfileEditForm


# Create your views here.
User = get_user_model()

def sign_up(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_normalUser = True
            user.save()
            profile = User.objects.get(username=user.username)
            
            profile.userprofile.gender = profile_form.cleaned_data.get('gender')
            profile.userprofile.age = profile_form.cleaned_data.get('age')
            profile.userprofile.blood_group = profile_form.cleaned_data.get('blood_group')
            profile.userprofile.phone = profile_form.cleaned_data.get('phone')
            profile.userprofile.address = profile_form.cleaned_data.get('address')

            profile.userprofile.save()

            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            return redirect('accounts:login')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/user/user_signup.html', context)

def login_view(request):
    if request.method == "POST":
        userlogin_form = UserLoginForm(request.POST)

        if userlogin_form.is_valid():
            username = userlogin_form.cleaned_data.get('username')
            password = userlogin_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)

            if user.is_normalUser:
                return redirect('core:user_dashboard')
                print('logged in')
            elif user.is_staffUser:
                return redirect('core:staff_dashboard')

            return redirect('core:index')
    else:
        userlogin_form = UserLoginForm()
    context = {
        'userlogin_form': userlogin_form
    }
    return render(request, 'accounts/user/user_login.html', context)

def logout_view(request):
    logout(request)
    return redirect('core:index')

def user_profile_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        userprofile_form = UserProfileEditForm(instance=request.user.userprofile, data=request.POST)

        if user_form.is_valid() and userprofile_form.is_valid():
            user_form.save()
            userprofile_form.save()

            return redirect('core:user_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        userprofile_form = UserProfileEditForm(instance=request.user.userprofile)

    context = {
        'user_form': user_form,
        'userprofile_form': userprofile_form,
    }
    return render(request, 'accounts/user/user_profile_edit.html', context)
