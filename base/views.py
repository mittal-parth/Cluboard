from django.shortcuts import render, redirect
from base.models import Club
from django.contrib.auth.models import User

from .forms import *

# Create your views here.


def index(request):

    clubs = Club.objects.all()
    context = {'clubs': clubs}
    return render(request, 'index.html', context)


def club_add(request):

    #Adding a new club
    form = ClubForm()
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'club_add.html', context)


def clubview(request, pk):
    # Display all users belonging to that club
    club = Club.objects.get(id=pk)
    members = club.users.all()
    context = {'club': club, 'members': members}

    return render(request, 'clubview.html', context)
