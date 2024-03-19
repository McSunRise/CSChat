from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import django.db.utils
from .forms import *


def home(request):
    return render(request, "home.html")


def reg(request):
    if request.method == "GET":
        return render(request, "reg.html", context={'form': RegForm})
    else:
        form = RegForm(request.POST)
        if form.is_valid():
            if form.pass_check():
                try:
                    user = form.save()
                    user.set_password(form.cleaned_data['password1'])
                    user.save()
                except django.db.utils.IntegrityError:
                    form.add_error('username', 'Пользователь с таким именем уже существует')
                    return render(request, "reg.html", context={'form': form})
            else:
                form.add_error('password1', 'Пароли не совпадают')
        else:
            form.add_error(None, 'Форма не заполнена')
    return redirect('/', permanent=True)


def login_page(request):
    if request.method == "GET":
        return render(request, "login.html", context={'form': LogForm})
    else:
        form = LogForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is None:
                form.add_error('password', 'Неправильно введён логин или пароль')
                return render(request, 'reg.html', context={'form': form})
            login(request, user)
        return redirect("/", permanent=True)


def logout_page(request):
    logout(request)
    return redirect("/", permanent=True)


def room(request, room_name):
    return render(request, 'chat_room.html', {'room_name': room_name})
