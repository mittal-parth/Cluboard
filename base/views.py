from django.shortcuts import render
from base.models import Club
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    clubs = Club.objects.all()
    context = {'clubs':clubs}
    return render(request, 'index.html',context)

def clubview(request, pk):
    #Display all users belonging to that club
    club = Club.objects.get(id = pk)
    members = club.users.all()
    context = {'club': club, 'members':members}

    return render(request, 'clubview.html', context)