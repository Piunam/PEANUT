from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest

# Create your views here.

def login(request):
    return render(request,'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

def profile(request:HttpRequest):
    return HttpResponse('Hello!')