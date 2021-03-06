from email.headerregistry import Group
import json
from urllib import request
from django.shortcuts import render, redirect
from matplotlib import use
from matplotlib.style import context
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout as logoutUser
from numpy import cumprod
from onlineMobileStore.models import *
from django.core.mail import send_mail

from django.http import JsonResponse
import random
from . import models


# Create your views here.
def addProduct(request):
    
        #return redirect('home')
    return render(request, 'add.html')

def index(request):
    if request.user.is_authenticated:
        #customer = models.Customer.objects.get(user_id=request.user.id)
        # customer = request.user.customer
        # order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # items = order.orderitem_set.all()
        # cartItems = order.get_cart_items
        cartItems = Cart.objects.filter(user_id=request.user.id).count()
    else:
        # items = []
        # order = {'get_cart_total':0, 'get_cart_items':0}
        # cartItems = order['get_cart_items']
        cartItems = 0
    

    topSale = Product.objects.all()
    context = {'topSale': topSale, 'cartItems':cartItems}

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



def cart(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     print(created)
    #     items = order.orderitem_set.all()
    #     print(items)
    # else:
    #     items = []
    #     order = {'get_cart_total':0, 'get_cart_items':0}
    customer = models.Customer.objects.get(user_id=request.user.id)

    cart = Cart.objects.filter(user_id=customer)
    context = {'cart':cart}

    return render(request, 'c.html', context);

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
        mobile = request.POST["mobile"]
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
        customer = Customer()
        customer.user = myUser
        customer.uname = uname
        customer.email = email
        customer.mobile = mobile
        customer.save()
        
        # subject = "Thanks for Register"
        # message = "Hey " + uname + " You are now successfully register with us and your password is secure"
        # to = email
        # send_mail(subject, message, 'no-reply@onlinestore.com', [to])
        # messages.success(request, "Your account has been successfully created")
        return redirect('login')
    return render(request, 'register.html')

def logout(request):
    logoutUser(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('home')

def updateItem(request):
    data = json.loads(request.body)

    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    print(orderItem.quantity)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item Added", safe=False)

def searchItem(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        print(query)
        if query:
            products = Product.objects.filter(name__icontains=query) 
            print(products)
            return render(request, 'search.html', {'products':products})
        else:
            print("No information to show")
            return render(request, 'search.html', {})

def productView(request, prod_slug):
    if(Product.objects.filter(slug=prod_slug, status=0)):
        products = Product.objects.filter(slug=prod_slug, status=0).first
        
        context = {'products': products}
    else:
        messages.error(request, "No such product found")
        return redirect('home')
    return render(request, 'product-detail.html', context)

def addToCart(request):
    if request.method == "POST":
        
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            print(prod_id)
            product_check = Product.objects.get(id=prod_id)
            if(product_check):
                customer = models.Customer.objects.get(user_id=request.user.id)
                if(Cart.objects.filter(user=customer, product_id=prod_id)):
                    return JsonResponse({'status':"Product Already in cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=customer, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status':'Product added successfully'})
                    else:
                        return JsonResponse({'status':"Only"+str(product_check.quantity)+" quantity availabel"})
            else:
                return JsonResponse({'status':"No such product found"})
        else:
            return JsonResponse({'status':'Login to Continue'})
    return render(request, 'login.html')

def updateCart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        print(prod_id)
        customer = models.Customer.objects.get(user_id=request.user.id)
        if(Cart.objects.filter(user=customer, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=customer)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status':"Update Successfully"})
    return redirect('home')

def deleteCartItem(request):
    if request.method == "POST":
        customer = models.Customer.objects.get(user_id=request.user.id)
        prod_id = int(request.POST.get('product_id'))
        if (Cart.objects.filter(user=customer, product_id=prod_id)):
            cartItem = Cart.objects.get(product_id=prod_id, user=customer)
            cartItem.delete()
        return JsonResponse({'status':"Deleted Successfully"})
    return redirect('home')

def checkout(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    rawCart = Cart.objects.filter(user=customer)
    for item in rawCart:
        if item.product_qty > item.product.quantity:
            Cart.objects.filter(id=item.id).delete()

    cartItem = Cart.objects.filter(user=customer)
    total_price = 0
    for item in cartItem:
        total_price = total_price + item.product.selling_price * item.product_qty

    context = {'cartItem': cartItem, 'total_price': total_price}
    return render(request, "checkout.html", context)

def placeOrder(request):
    if request.method == "POST":
        customer = models.Customer.objects.get(user_id=request.user.id)
        newOrder = Order()
        newOrder.user = request.user
        newOrder.fname = request.POST.get('fname')
        newOrder.lname = request.POST.get('lname')
        newOrder.email = request.POST.get('email')
        newOrder.phone = request.POST.get('phone')
        newOrder.address = request.POST.get('address')
        newOrder.city = request.POST.get('city')
        newOrder.state = request.POST.get('state')
        newOrder.country = request.POST.get('country')
        newOrder.pincode = request.POST.get('pincode')

        newOrder.payment_mode = request.POST.get('payment_mode')

        cart = Cart.objects.filter(user=customer)
        cart_total_price = 0

        for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.product_qty
        
        newOrder.total_price = cart_total_price
        trackno = 'gurau'+str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'gurau'+str(random.randint(1111111, 9999999))

        newOrder.tracking_no = trackno
        newOrder.save()

        newOrderItems = Cart.objects.filter(user=customer)
        for item in newOrderItems:
            OrderItem.objects.create(
                order = newOrder,
                product = item.product,
                price = item.product.selling_price,
                quantity = item.product_qty
            )

            orderProduct = Product.objects.filter(id=item.product_id).first()
            orderProduct.quantity = orderProduct.quantity - item.product_qty
            orderProduct.save()

        Cart.objects.filter(user=customer).delete()

        #messages.success(request, "Your order has been placed Successfully")
        payMode = request.POST.get('payment_mode')
        if (payMode == "Paid by PayPal"):
            return JsonResponse({'status':"Your order has been placed successfully"})
        else:
            messages.success(request, "Your order has been placed Successfully")

    return redirect('home')

def paypalCheck(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    cart = Cart.objects.filter(user=customer)
    total_price = 0
    for item in cart:
        total_price = total_price + item.product.selling_price * item.product_qty

    return JsonResponse({
        'total_price': total_price
    })

def myOrder(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, "orders.html", context)

def viewOrder(request, t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderItems = OrderItem.objects.filter(order=order)
    context = {'order':order, 'orderitems':orderItems}
    return render(request, 'vieworders.html', context)

def category(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'category.html', context)


############Admin Panel##############
def adminPanel(request):
    customerCount = models.Customer.objects.all().count()
    productCount = models.Product.objects.all().count()
    orderCount = models.Order.objects.all().count()

    myDict = {
        'customerCount':customerCount,
        'productCount':productCount,
        'orderCount':orderCount,
    }
    return render(request, "admin/admin-dashboard.html", context=myDict)


def adminLogIn(request):
    return render(request, "admin/admin-login.html")

def productsAdd(request):
    return render(request, "admin/add-products.html")

def products(request):
    products = models.Product.objects.all()
    return render(request, "admin/products.html", {"products":products})

def purchaseList(request):
    return render(request, "admin/purchase-list.html")

def viewCustomers(request):
    customers = models.Customer.objects.all()

    return render(request, "admin/view-customers.html", {"customers":customers})

def updateProduct(request, pk):
    prodUpdate = Product.objects.get(id=pk)

    if request.method == "POST":
        prodUpdate.category = request.POST.get('category')
        prodUpdate.slug = request.POST.get('slug')
        prodUpdate.name = request.POST.get('name')
        if len(request.FILES) != 0:
            prodUpdate.image = request.FILES['image']
        prodUpdate.small_description = request.POST.get('s-des')
        prodUpdate.qunatity = request.POST.get('quantity')
        prodUpdate.original_price = request.POST.get('o-price')
        prodUpdate.selling_price = request.POST.get('s-price')
        prodUpdate.trending = request.POST.get('trending')
        prodUpdate.save()
        
        return redirect('product-update')

    context = {'prodUpdate':prodUpdate}
    return render(request, "admin/product-update.html", context=context)

def deleteProduct(request, pk):
    prod = Product.objects.get(id=pk)
    
    prod.delete()
    
    return redirect('products')