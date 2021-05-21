from django.shortcuts import render, redirect
from base.models import Club
from django.contrib.auth.models import User

from .forms import *

from math import ceil
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


def item_add(request, pk):

    club = Club.objects.get(id=pk)
    initial = {'club':club}
    #Adding a new item
    form = ItemForm(initial=initial)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'club':club, 'form':form}
    return render(request, 'item_add.html', context)


def club_view(request, pk):
    # Display all users belonging to that club
    club = Club.objects.get(id=pk)
    members = club.users.all()
    context = {'club': club, 'members': members}

    return render(request, 'club_view.html', context)

def items_view(request, pk):
    #Display all items belonging to that club as a carousel of cards
    club = Club.objects.get(id=pk)
    items = club.item_set.all()
    all_items = []
    n = len(items)
    nSlides = n//4 + ceil(n/4-n//4) #logic for displaying slides
    all_items.append([items, range(1, nSlides), nSlides])

    context = {'club':club, 'all_items':all_items}
    return render(request, 'items_view.html', context)
