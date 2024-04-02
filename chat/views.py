from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *


def home(request):
    return render(request, "home.html")


def reg(request):
    if request.method == "GET":
        return render(request, "reg.html", context={'form': RegForm, 'feedback_form': FeedbackForm})
    else:
        form = RegForm(request.POST)
        feedback_form = FeedbackForm(request.POST)
        if form.is_valid():
            if form.pass_check():
                user = form.save()
                user.set_password(form.cleaned_data['password1'])
                user.save()
            else:
                form.add_error('password1', 'Пароли не совпадают')
                return render(request, "reg.html", context={'form': form, 'feedback_form': FeedbackForm})
        else:
            return render(request, "reg.html", context={'form': form, 'feedback_form': FeedbackForm})
        if feedback_form.is_valid():
            pass  # TODO: Логика отправки фидбека
            return render(request, "reg.html", context={'form': form, 'feedback_form': FeedbackForm})
    return redirect('/', permanent=True)


def login_page(request):
    if request.method == "GET":
        return render(request, "login.html", context={'form': LogForm, 'feedback_form': FeedbackForm})
    else:
        form = LogForm(request.POST)
        feedback_form = FeedbackForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is None:
                form.add_error('password', 'Неправильно введён логин или пароль')
                return render(request, 'login.html', context={'form': form, 'feedback_form': FeedbackForm})
            login(request, user)
        if feedback_form.is_valid():
            pass  # TODO: Логика отправки фидбека
            return render(request, 'login.html', context={'form': form, 'feedback_form': FeedbackForm})
        return redirect("/", permanent=True)


def logout_page(request):
    logout(request)
    return redirect("/", permanent=True)


def pass_restore(request):
    if request.method == "GET":
        return render(request, 'restore.html', context={'form': PassRestoreForm})
    else:
        form = PassRestoreForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username__exact=form.cleaned_data['username'])
            except User.DoesNotExist:
                form.add_error('username', 'Пользователя не существует')
                return render(request, 'restore.html', context={'form': form})
            if user.check_password(form.cleaned_data['new_password']):
                form.add_error('new_password', 'Новый пароль не может совпадать со старым')
                return render(request, 'restore.html', context={'form': form})
            user.set_password(form.cleaned_data['new_password'])
            user.save()
        return redirect("/", permanent=True)


def room(request, room_name):
    return render(request, 'chat_room.html', {'room_name': room_name})
