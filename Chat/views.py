from django.shortcuts import render
import psycopg2

def home(request):
    return render(request, "home.html")

# Create your views here.
