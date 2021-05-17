from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
 
    return render(request, 'login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')