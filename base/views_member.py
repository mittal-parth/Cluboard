from django.shortcuts import render, redirect
from django.urls import reverse
from base.models import Club, Request, Item
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import *

from math import ceil

#Views that are exclusively for a Member are implemented here 
def index_member(request, pk):
    #Display all items belonging to that club as a carousel of cards
    club = Club.objects.get(id=pk)
    items = club.item_set.all()
    all_items = []
    n = len(items)
    nSlides = n//4 + ceil(n/4-n//4) #logic for displaying slides
    all_items.append([items, range(1, nSlides), nSlides])

    #Display all requests made by that user
    reqs = request.user.request_set.all()

    context = {'club':club, 'all_items':all_items, 'reqs':reqs}
    return render(request, 'index_member.html', context)

def request_add(request, pk):
    club = Club.objects.get(id = pk)

    #Pre-filling a form with required values
    initial = {'requested_by':request.user, 'club':club, 'status':'Pending'}
    form = RequestForm(initial=initial)

    #Restrict what a member can choose from
    #Only see items pertaining to member's club
    form.fields['item'].queryset = Item.objects.filter(club = pk)
    form.fields['club'].queryset = Club.objects.filter(id = pk)
    form.fields['requested_by'].queryset = User.objects.filter(username = request.user)

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('index_member', args = [pk]))
    context = {'club':club, 'form':form}
    return render(request, 'request_add.html', context)