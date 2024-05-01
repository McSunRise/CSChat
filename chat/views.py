import django.db.utils
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import Message, Chat, User


def home(request):
    messages = (Message.objects.filter(author=request.user) | Message.objects.filter(receiver=request.user)).order_by(
        'chat_id', '-pub_date').distinct('chat__id')
    chats = Chat.objects.filter(members=request.user)
    return render(request, "home.html", context={'chats': chats, 'messages': messages})


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
        first_chat = Chat.objects.create(pk=user.pk)
        first_chat.save()
        message = Message.objects.create(chat=user.pk, author=user, receiver=user, message='For testing purposes')
        message.save()
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


def chat_create(request):
    if request.method == "GET":
        return render(request, 'chat_create.html', context={'form': ChatCreateForm})
    else:
        form = ChatCreateForm(request.POST)
        if form.is_valid():
            receiver = User.objects.get(username=form.cleaned_data['receiver'])
            chat = Chat.objects.create()
            chat.members.add(request.user, receiver)
            # TODO: Дописать эту хуергу
            print(chat.members.values())
            print(Chat.objects.filter(members=request.user)[0].members.values())
            print(chat.members.values() != Chat.objects.filter(members=request.user)[0].members.values())
            if chat.members not in Chat.objects.values('members'):
                chat.save()
                first_mes = Message.objects.create(chat=chat, author=request.user, receiver=receiver, message='First message in a new chat. Write something!')
                first_mes.save()
        return redirect("/", permanent=True)


def room(request, room_name):
    if request.user.id in Chat.objects.get(pk=room_name).members.all().values_list(flat=True):
        return render(request, 'chat_room.html',
                      context={'room_name': room_name, 'message_list': Message.objects.filter(chat=room_name)})
    else:
        return redirect("/", permanent=True)
