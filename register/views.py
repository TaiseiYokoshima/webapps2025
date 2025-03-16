from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import login


from . forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # Login the user after registration
            return redirect('home')  # Redirect to homepage after login
    else:
        form = RegisterForm()
    
    return render(request, 'register/register.html', {'form': form})


def index(request):
    return HttpResponse("hello, world. you are at index")

