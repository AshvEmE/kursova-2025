from django.shortcuts import render
from .models import Task


def index(request):
    tasks = Task.objects.all()
    return render(request,'main/index.html', {'title': 'Main site page', 'tasks': tasks})

def dashboard(request):
    return render(request,'main/dashboard.html')

