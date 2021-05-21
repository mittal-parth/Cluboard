from django.contrib import admin
from django.urls import path
from base import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("club_add/", views.club_add, name="club_add"), 
    path("item_add/<int:pk>", views.item_add, name="item_add"), 
    path("items_view/<int:pk>", views.items_view, name="items_view"), 
    path("club_view/<int:pk>", views.club_view, name="club_view"), 
]
