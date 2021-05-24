from django.shortcuts import render, redirect
from django.urls import reverse
from base.models import Club, Request, Item
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import *

from math import ceil

#Views that are exclusively for a Convenor are implemented here 
def request_approve(request, request_id):
    #Approve the request if there is sufficient quantity available
    req = Request.objects.get(id = request_id)
    club_id = req.item.club.id 
    if req.item.qty - req.qty >= 0:
        req.item.qty -= req.qty
        req.status = 'Approved'
        req.item.save()
        req.save()
        messages.success(request, 'Request approved successfully!')
        return redirect(reverse('items_view', args = [club_id]))
    else:
        messages.info(request, 'Request cannot be approved - Insufficient Quantity')
        return redirect(reverse('items_view', args = [club_id]))

def request_reject(request, request_id):
    req = Request.objects.get(id = request_id)
    club_id = req.item.club.id 
    req.status = 'Rejected'
    req.save()
    messages.info(request, 'Request rejected successfully!')
    return redirect(reverse('items_view', args = [club_id]))