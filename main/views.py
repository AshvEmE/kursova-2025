from django.shortcuts import redirect, render


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'main/index.html')

def dashboard(request):
    return render(request,'main/dashboard.html')

