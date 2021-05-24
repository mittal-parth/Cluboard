from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

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


    return render(request, 'signup.html')
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have been successfully logged in!')
            if user.info.designation == 'Admin':
                return redirect('/')
            elif user.info.designation == 'Convenor':
                return redirect(reverse('club_view', args = [user.club_set.first().id]))
            else:
                return redirect(reverse('index_member', args = [user.club_set.first().id]))
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
 
    return render(request, 'login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request, 'profile.html')