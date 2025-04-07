from django.shortcuts import render

from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

from django.shortcuts import render, redirect

@login_required
def home(request):
    return HttpResponse("Welcome Home!")

@login_required
def sign_out(request):
    logout(request)
    return redirect('login')

    


