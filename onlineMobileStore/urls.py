from django.contrib import admin
from django.urls import path
from onlineMobileStore import views

urlpatterns = [
    path("", views.index, name='home'),
    path("cart", views.cart, name='cart'),
    path("product", views.product, name='product'),
    path("login", views.handleLogin, name='login'),
    path("register", views.register, name='register'),
    path("logout", views.logout, name='logout')
]