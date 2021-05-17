from django.shortcuts import render
from base.models import Club
# Create your views here.
def index(request):
    clubs = Club.objects.all()
    context = {'clubs':clubs}
    return render(request, 'index.html',context)

def clubview(request, pk):
    club = Club.objects.filter(id = pk)
    context = {'club': club[0]}

    return render(request, 'clubview.html', context)