from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from accounts import views

urlpatterns = [
    path("signup", views.signupPage, name= "signup"),
    path("login", views.loginPage, name= "login"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("logout", views.logoutPage, name= "logout"),

    #They are url names and view functions are provided by default by Django
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name = 'password_reset.html'), name="password_reset"), 
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'), name="password_reset_done"), 
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html'), name="password_reset_confirm"), 
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'), name="password_reset_complete"),

    path('password_change', auth_views.PasswordChangeView.as_view(template_name = 'password_change.html'), name="password_change"), 
    path('password_change_done', auth_views.PasswordChangeDoneView.as_view(template_name = 'password_change_done.html'), name="password_change_done"), 
]
