from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import django.db.utils
from chat.models import User
import psycopg2

def home(request):
    return render(request, "home.html", context={'user_logged': True})

def reg(request):
    if request.method == "GET":
        return render(request, "reg.html")
    else:
        data = request.POST
        username = data['username']
        email = data['email']
        password, password2 = data['password'], data['password2']
        if password != password2:
            return render(request, "reg.html", context={'passwords': False})
        newuser = User()
        try:
            newuser.create_user(username=username, email=email, password=password)
        except django.db.utils.IntegrityError:
            return render(request, "reg.html", context={'user_exist': True})
        login(request, newuser)
        return redirect('/', permanent=True)

def login_page(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        data = request.POST
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            return render(request, "login.html", context={"valid_data": False})
        login(request, user)
        return redirect('/', permanent=True)

def logout_page(request):
    logout(request)
    return redirect('/', permanent=True)

# Create your views here.