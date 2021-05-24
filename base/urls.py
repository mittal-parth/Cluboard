from django.contrib import admin
from django.urls import path
from base import views, views_admin, views_convenor, views_member

urlpatterns = [
    path("", views_admin.index, name="index"), 
    path("index_member/<int:pk>", views_member.index_member, name="index_member"), 
    path("club_add/", views_admin.club_add, name="club_add"), 
    path("item_add/<int:pk>", views.item_add, name="item_add"), 
    path("request_add/<int:pk>", views_member.request_add, name="request_add"), 
    path("items_view/<int:pk>", views.items_view, name="items_view"), 
    path("club_view/<int:pk>", views.club_view, name="club_view"), 
    path("request_approve/<int:request_id>", views_convenor.request_approve, name="request_approve"), 
    path("request_reject/<int:request_id>", views_convenor.request_reject, name="request_reject"), 
]
