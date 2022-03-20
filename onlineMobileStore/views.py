from django.shortcuts import render, redirect
from matplotlib.style import context
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout as logoutUser
from onlineMobileStore.models import Sale, SpecialPrice
from django.core.mail import send_mail


# Create your views here.
def addProduct(request):
    
        #return redirect('home')
    return render(request, 'add.html')

def index(request):
    topSale = Sale.objects.all()
    context = {'topSale': topSale}

    return render(request, 'index.html', context);


def editProduct(request, pk):
    prod = Sale.objects.get(id=pk)

    if request.method == "POST":
        if len(request.FILES) != 0:
            prod.image = request.FILES['image']
        prod.p_name = request.POST.get('name')
        prod.price = request.POST.get('price')
        prod.save()
        
        return redirect('view')

    context = {'prod':prod}
    return render(request, 'update.html', context)

def deleteProduct(request, pk):
    prod = Sale.objects.get(id=pk)
    
    prod.delete()
    
    return redirect('view')

def cart(request):
    return render(request, 'cart.html');

def view(request):
    if request.method == "POST":

        
        image = request.FILES['image']
    
        name = request.POST['name']
        price = request.POST['price']
        
        prod = Sale(
            image = image,
            p_name = name,
            price = price
        )

        
        prod.save()
        return redirect('view')
    topSale = Sale.objects.all()
    context = {'topSale': topSale}

    return render(request, 'view.html', context)

def onSale(request):
    return render(request, 'onSale.html');

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

        subject = "Thanks for Register"
        message = "Hey " + uname + " You are now successfully register with us and your password is secure"
        to = email
        send_mail(subject, message, 'no-reply@onlinestore.com', [to])
        messages.success(request, "Your account has been successfully created")
        return redirect('login')
    return render(request, 'register.html')

def logout(request):
    logoutUser(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')

