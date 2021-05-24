from django.shortcuts import render, redirect
from django.urls import reverse
from base.models import Club, Request, Item
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import *

from math import ceil

# Views that are common to a Convenor and Admin are implemented here

def item_add(request, pk):

    club = Club.objects.get(id=pk)
    initial = {'club':club}
    #Adding a new item
    form = ItemForm(initial=initial)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('items_view', args = [pk]))
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

    #Display all requests pertaining to that club
    reqs = club.request_set.all()

    context = {'club':club, 'all_items':all_items, 'reqs':reqs}
    return render(request, 'items_view.html', context)

def item_update(request, item_id):
    #Update an existing item

    item = Item.objects.get(id = item_id)
    form = ItemForm(instance = item)
    form.fields['club'].queryset = Club.objects.filter(id = item.club.id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance = item)
        if form.is_valid():
            item.save()
            return redirect(reverse('items_view', args=[item.club.id])) 

    context = {'form':form}
    return render(request, 'item_update.html',context)
