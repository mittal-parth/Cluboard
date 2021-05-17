from django.shortcuts import render
from base.models import Club
# Create your views here.
def index(request):
    clubs = Club.objects.all()
    context = {'clubs':clubs}
    return render(request, 'index.html',context)