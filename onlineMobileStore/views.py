from django.shortcuts import render, redirect, HttpResponse
from matplotlib.style import context
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout as logoutUser


# Create your views here.
def index(request):
    return render(request, 'index.html');

def cart(request):
    return render(request, 'cart.html');

def product(request):
    return render(request, 'product.html');

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST["loginemail"]
        loginpassword = request.POST["loginpassword"]

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successfully")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials, Please try again")
            return redirect('login')

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        #Get post parameters
        uname = request.POST["username"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        repass = request.POST["repass"]

        #validation
        if len(uname) > 10:
            messages.error(request, "User name must be under 10 characters")
            return redirect('register')
        
        if not uname.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('register')

        if pass1 != repass:
            messages.error(request, "Password do not match")
            return redirect('register')
        #create the user
        myUser = User.objects.create_user(uname, email, pass1)
        myUser.first_name = uname
        myUser.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('login')
    return render(request, 'register.html')

def logout(request):
    logoutUser(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')
