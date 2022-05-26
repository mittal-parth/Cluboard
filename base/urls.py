from django.contrib import admin
from django.urls import path
from base import views

urlpatterns = [
    path("", views.index, name="index"),

    path("club_view/<int:pk>", views.club_view, name="club_view"), 
    path("club_add/", views.club_add, name="club_add"), 

    path("user_add/<int:pk>", views.user_add, name="user_add"), 
    path("user_delete/<int:user_id>", views.user_delete, name="user_delete"), 

    path("item_add/<int:pk>", views.item_add, name="item_add"), 
    path("item_update/<int:pk>/<int:item_id>", views.item_update, name="item_update"), 
    path("item_delete/<int:item_id>", views.item_delete, name="item_delete"), 
    path("items_view/<int:pk>", views.items_view, name="items_view"), 

    path("request_add/<int:pk>", views.request_add, name="request_add"),   
    path("request_approve/<int:request_id>", views.request_approve, name="request_approve"), 
    path("request_reject/<int:request_id>", views.request_reject, name="request_reject"), 

    path("error_page/", views.error_page, name="error_page"),    
]
