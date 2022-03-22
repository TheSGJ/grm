from django.contrib import admin
from django.contrib import admin
from django.urls import path, include
from tv import views



urlpatterns = [
    path('postComment', views.postComment, name="postComment"),
    path("", views.tvHome, name='tvHome'),
    path("<str:slug>", views.tvPost, name='tvPost'),
]