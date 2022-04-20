from unicodedata import name
from django.contrib import admin
from django.urls import path
import nacl
from onlineMobileStore import views

urlpatterns = [
    path("", views.index, name='home'),
    path("cart", views.cart, name='cart'),
    path("product", views.product, name='product'),
    path("login", views.handleLogin, name='login'),
    path("register", views.register, name='register'),
    path("logout", views.logout, name='logout'),
    path("onsale", views.onSale, name='onsale'),
    path('editProduct/<str:pk>', views.editProduct, name="edit-prod"),
    path('view', views.view, name='view'),
    path('delete-product/<str:pk>', views.deleteProduct, name="delete-prod"),

    path("update-item", views.updateItem, name="update-item"),

    path("search", views.searchItem, name='search'),
    path("product-detail/<str:prod_slug>", views.productView, name='product-detail'),

    path('add', views.addToCart, name="addtocart"),
    path('update-cart', views.updateCart, name="update-cart"),
    path('delete-cart-item', views.deleteCartItem, name='delete-cart-item'),

    path('checkout', views.checkout, name="checkout"),
    path('placeOrder', views.placeOrder, name="placeOrder"),
    path('proceed-to-pay', views.paypalCheck, name='proceed-to-pay'),

    path('my-order', views.myOrder, name='my-order'),
    path('view-order/<str:t_no>', views.viewOrder, name='view-order'),

    path('category', views.category, name='category'),

    #Admin url
    path('admin-panel', views.adminPanel, name='admin-panel'),
    path('admin-login', views.adminLogIn, name='admin-login'),
    path('add-products', views.productsAdd, name='add-products'),
    path('products', views.products, name='products'),
    path('purchase-list', views.purchaseList, name="purchase-list"),
    path('view-customers', views.viewCustomers, name='view-customers'),

    path('update-product/<str:pk>',views.updateProduct, name='update-product'),
    path('delete-product/<str:pk>',views.deleteProduct, name='delete-product'),
]