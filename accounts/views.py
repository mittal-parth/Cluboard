from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounts.models import Info 
from base.models import Club
from .forms import CreateUserForm
# Create your views here.


def signupPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created for '+ user)
            return redirect('login')
        
    context = {'form':form}
    return render(request, 'signup.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have been successfully logged in!')
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
 
    return render(request, 'login.html')

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request, pk, user_id):
    user = User.objects.get(id = user_id)
    club = Club.objects.get(id = pk)
    context = {'club':club, 'user':user}
    if request.user.info.designation == 'Member':
        if request.user.id == user_id:
            return render(request, 'profile.html', context)
        else:
            return redirect('error_page')
    elif request.user.info.designation == 'Convenor':
        if request.user.club_set.first().id == club.id:
            return render(request, 'profile.html', context)
        else:
            return redirect('error_page')
    return render(request, 'profile.html', context)


