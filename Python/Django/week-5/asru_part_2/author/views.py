from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from posts.models import Post


# Create your views here.
def register(request):
    if request.method == "POST":
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, "Account Created Successfully")
            return redirect("register")
    else:
        register_form = forms.RegistrationForm()

    return render(request, "register.html", {"form": register_form, "type": "Register"})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user_name = form.cleaned_data["username"]
            user_pass = form.cleaned_data["password"]

            user = authenticate(username=user_name, password=user_pass)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("home")
            else:
                messages.warning(request, "Login informtion incorrect")
                return redirect("register")
    else:
        form = AuthenticationForm()
    return render(request, "register.html", {"form": form, "type": "Login"})


@login_required
def profile(request):
    data = Post.objects.filter(author = request.user)
    return render(request, "profile.html", {"data": data})


@login_required
def edit_profile(request):
    if request.method == "POST":
        profile_form = forms.ChangeUserData(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "update profile Successfully")
            return redirect("profile")
    else:
        profile_form = forms.ChangeUserData(instance=request.user)
    return render(request, "update_profile.html", {"form": profile_form})


def pass_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "update profile Successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "passchange.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("user_login")
