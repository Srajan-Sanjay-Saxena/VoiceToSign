"""A2SL URL Configuration"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('animation/', views.animation_view, name='animation'),
    path('api/animation/', views.api_animation_view, name='api_animation'),
    path('api/transcribe/', views.transcribe_view, name='transcribe'),
    path('', views.home_view, name='home'),
]
