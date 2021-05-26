from django.db.models import query
from django.shortcuts import render, HttpResponse, redirect
from .models import Product,Order,OrderUpdate
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from math import ceil
from django.contrib.auth.decorators import login_required
import json

def index(request):
    products=Product.objects.all()
    return render(request, 'hardware/index.html', {'product':products})

def productview(request,proid):
    product=Product.objects.filter(id=proid)
    return render(request, 'hardware/prod_view.html', {'product':product[0]})

def signup(request):
    if request.method=="POST":
        username=request.POST.get('username', '')
        email=request.POST.get('email', '')
        pass1=request.POST.get('password', '')

        # check for errorneous input
        if len(username)<5:
            messages.error(request, " Your user name must be above 5 characters")
            return redirect('/hardware/')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, " Your account has been successfully created")
        return redirect('/hardware/')

    return render(request, 'hardware/signup.html')

def handlelogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/hardware/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/hardware/")

    return render(request, 'hardware/login.html')

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/hardware/')


def searchMatch(query,item):
    query=query.lower()
    if query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.sub_category.lower():
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search')
    if(query==""):
        return redirect("/hardware/")
    else:
        products=Product.objects.all()
        prod=[item for item in products if searchMatch(query, item)]
        return render(request, 'hardware/search.html', {'product':prod})

def tracker(request):
    if not request.user.is_authenticated:
        return redirect("/hardware/login/")
    else:
        if request.method=="POST":
            orderId = request.POST.get('orderId', '')
            email = request.POST.get('email', '')
            try:
                order = Order.objects.filter(order_id=orderId, email=email)
                if len(order)>0:
                    update = OrderUpdate.objects.filter(order_id=orderId)
                    updates = []
                    for item in update:
                        updates.append({'text': item.update_desc, 'time': item.timestamp})
                        response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                    return HttpResponse(response)
                else:
                    return HttpResponse('{"status":"noitem"}')
            except Exception as e:
                return HttpResponse('{"status":"error"}')
    return render(request, 'hardware/tracker.html')


def checkout(request):
    if not request.user.is_authenticated:
        return redirect("/hardware/login/")
    else:
        if request.method=="POST":
            items_json= request.POST.get('itemsJson', '')
            name=request.POST.get('name', '')
            amount = request.POST.get('amount', '')
            email=request.POST.get('email', '')
            address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
            city=request.POST.get('city', '')
            state=request.POST.get('state', '')
            zip_code=request.POST.get('zip_code', '')
            phone=request.POST.get('phone', '')

            order = Order(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
            order.save()
            update=OrderUpdate(order_id=order.order_id,update_desc="The order has been placed")
            update.save()
            id=order.order_id
            orderPlaced=True
            messages.success(request, f"Your Order has been placed you can track your order here using your Order Id {id}")
            return render(request, 'hardware/tracker.html', {'orderPlaced':orderPlaced})
    return render(request, 'hardware/checkout.html')


def searchCategory(query,item):
    if query in item.category.lower():
        return True
    else:
        return False

def categoryClick(request,ctgry):
    query=ctgry.lower()
    products=Product.objects.all()
    prod=[item for item in products if searchCategory(query, item)]
    return render(request, 'hardware/search.html', {'product':prod})