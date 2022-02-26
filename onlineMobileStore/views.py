from django.shortcuts import render, HttpResponse
from matplotlib.style import context

# Create your views here.
def index(request):
    return render(request, 'index.html');

def cart(request):
    return render(request, 'cart.html');

def product(request):
    return render(request, 'product.html');

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')