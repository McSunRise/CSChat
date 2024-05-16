from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Max, Count
from .forms import *
from .models import Message, Chat, User


def render_by_rn(request, messages, room_name, search_form=ChatCreateForm):
    if room_name != 0:
        if Chat.objects.get(pk=room_name).members.count() > 1:
            return render(request, "home.html", context={'messages': messages,
                                                         'room_name': room_name,
                                                         'search_form': search_form,
                                                         'message_list': Message.objects.filter(chat=room_name),
                                                         'receiver': [i['id'] for i in
                                                                      Chat.objects.get(pk=room_name).members.values(
                                                                          'id') if i['id'] != request.user.id][0]})
        else:
            return render(request, "home.html", context={'messages': messages,
                                                         'room_name': room_name,
                                                         'search_form': search_form,
                                                         'message_list': Message.objects.filter(chat=room_name),
                                                         'receiver': request.user.id})
    else:
        return render(request, "home.html", context={'messages': messages,
                                                     'room_name': room_name,
                                                     'search_form': search_form})


def chat_create(user, receiver):
    chat = Chat.objects.create()
    chat.members.add(user, receiver)
    chat.save()
    first_mes = Message.objects.create(chat=chat,
                                       author=user,
                                       receiver=receiver,
                                       message='First message in a new chat. Write something!'
                                       )
    first_mes.save()


def render_search(request, messages, room_name):
    if request.method == "GET":
        return render_by_rn(request, messages, room_name)
    else:
        search_form = ChatCreateForm(request.POST)
        if search_form.is_valid():
            try:
                receiver = User.objects.get(username=search_form.cleaned_data['receiver'])
            except User.DoesNotExist:
                search_form.add_error('receiver', 'Пользователя не существует')
                return render_by_rn(request, messages, room_name, search_form)
            user_chats = Chat.objects.filter(members=request.user.id)
            receiver_chats = Chat.objects.filter(members=receiver.id)
            if len(user_chats.intersection(receiver_chats)) == 0:
                chat_create(request.user, receiver)
            elif request.user == receiver:
                return redirect(f"/chat/{[i.id for i in user_chats if i.members.count() == 1][0]}")
            else:
                return redirect(f"/chat/{user_chats.intersection(receiver_chats)[0].id}", permanent=True)
        return redirect("/", permanent=True)


def home(request):
    messages = (Message.objects.filter(author=request.user) | Message.objects.filter(receiver=request.user)) \
        .filter(id__in=Message.objects.values('chat__id').annotate(id=Max('id')).values('id')).order_by('-pub_date')
    return render_search(request, messages, room_name=0)


def redir(request):
    return redirect("/chat", permanent=True)


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
        chat_create(user, user)
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
    messages = (Message.objects.filter(author=request.user) | Message.objects.filter(receiver=request.user)) \
        .filter(id__in=Message.objects.values('chat__id').annotate(id=Max('id')).values('id')).order_by('-pub_date')
    if request.user.id in Chat.objects.get(pk=room_name).members.all().values_list(flat=True):
<<<<<<< HEAD
        return render_search(request,messages, room_name)
=======
        return render_search(request, messages, room_name)
>>>>>>> backend-develop
    else:
        return redirect("/", permanent=True)
