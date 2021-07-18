
from django.contrib import admin
from django.urls import path
from . import views
  
urlpatterns = [
    path('', views.home),
    path('clear/', views.clearTable, name="delete"),
    path('photo/', views.capture, name="capture"),
    path('video/', views.test, name="test"),
    path('show/', views.home, name="show"),
]