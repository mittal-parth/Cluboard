from django.contrib import admin
from django.urls import path
from base import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("club_add/", views.club_add, name="club_add"), 
    path("clubview/<int:pk>", views.clubview, name="clubview"), 
]
