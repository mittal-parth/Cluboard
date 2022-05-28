from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count

from accounts.models import Info 
from base.models import Request
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
def profile(request, user_id):
    user = User.objects.get(id = user_id)
    
    # User clubs for bar chart
    clubs = user.club_set.all()
    clubs_list = list(clubs.values_list('club_name', flat=True))

    # Requests count by club
    user_requests = user.request_set.all()
    requests_count_by_club = list(user_requests.values('club').annotate(dcount = Count('club')).order_by().values_list('dcount', flat = True))
    
    # Request count by status for pie chart
    # status_choices =  sorted([status[0] for status in Request.status.field.choices])
    status_choices = list(user_requests.values('status').annotate(dcount = Count('status')).order_by().values_list('status', flat = True))
    requests_count_by_status = list(user_requests.values('status').annotate(dcount = Count('status')).order_by().values_list('dcount', flat = True))

    context = {'user':user, 'clubs': clubs, 'clubs_list':clubs_list, 'requests_count_by_club':requests_count_by_club, 'status_choices':status_choices, 'requests_count_by_status':requests_count_by_status}
    return render(request, 'profile.html', context)


