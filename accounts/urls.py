from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path("signup", views.signupPage, name= "signup"),
    path("login", views.loginPage, name= "login"),
    path("profile/<int:pk>/<int:user_id>", views.profile, name="profile"),
    path("logout", views.logoutPage, name= "logout"),
]
