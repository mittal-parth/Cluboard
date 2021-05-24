from django.shortcuts import render, redirect
from django.urls import reverse
from base.models import Club, Request, Item
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import *

from math import ceil

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