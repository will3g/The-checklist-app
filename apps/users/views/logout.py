from django.shortcuts import redirect
from django.contrib import auth

def logout(request):
    auth.logout(request=request)
    return redirect('index')
