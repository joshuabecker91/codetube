from django.shortcuts import render, redirect
from codetubeApp.models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    return render(request, 'search.html')

def login_reg(request):
    return render(request, 'login_reg.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def new_video(request):
    return render(request, 'new_video.html')

def edit_video(request):
    return render(request, 'edit_video.html')

def play(request):
    return render(request, 'play.html')
