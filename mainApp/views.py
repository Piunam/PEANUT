from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.

def login(request):
    return render(request,'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

def profile(request:HttpRequest):
    return HttpResponse('Hello!')


def logout_view(request):
    logout(request)  # This logs out the user
    return redirect('home')  # Redirect to the home page or login page