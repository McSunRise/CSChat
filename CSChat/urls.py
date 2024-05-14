"""
URL configuration for CSChat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from chat import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.redir, name='redir'),
    path("chat/", login_required(views.home), name='home'),
    path("auth/reg/", views.reg, name='registration'),
    path("auth/", views.login_page, name='login'),
    path("logout/", views.logout_page, name='logout'),
    path("auth/password_restore/", views.pass_restore, name='password_restore'),
    path("chat/<int:room_name>", login_required(views.room), name='room'),
    path("chat/create", login_required(views.chat_create), name='create')
]
