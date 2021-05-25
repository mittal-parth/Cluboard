from django.contrib import admin
from django.urls import path
from base import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("index_member/<int:pk>", views.index_member, name="index_member"), 
    path("club_add/", views.club_add, name="club_add"), 
    path("item_add/<int:pk>", views.item_add, name="item_add"), 
    path("item_update/<int:item_id>/<int:pk>", views.item_update, name="item_update"), 
    path("request_add/<int:pk>", views.request_add, name="request_add"), 
    path("items_view/<int:pk>", views.items_view, name="items_view"), 
    path("club_view/<int:pk>", views.club_view, name="club_view"), 
    path("request_approve/<int:request_id>", views.request_approve, name="request_approve"), 
    path("request_reject/<int:request_id>", views.request_reject, name="request_reject"), 
    path("error_page/", views.error_page, name="error_page"), 
]
