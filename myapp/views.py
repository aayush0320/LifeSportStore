import datetime
import os
import random

from django.contrib.sessions import serializers
from  django.core.mail import send_mail

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.auth.decorators import login_required, user_passes_test

from myapp import forms
from myapp.forms import OrderForm, InterestForm, LoginForm
from myapp.models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404
from django.shortcuts import render


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        testuser = request.user

    else:
        testuser = ""



    cat_list = Category.objects.all().order_by('id')[:10]  #query to print list of categories
    prod_list = Product.objects.all().order_by('-price')[:5]  #query to print list of product in descending order of price
    response = HttpResponse()
    heading1 = '<p>' + 'List of Categories: ' + '</p>'
    response.write(heading1)
    for category in cat_list:
        para = '<p>' + str(category.id) + ': ' + str(category.name) + '</p>'
        response.write(para)
    heading1 = '<p>' + 'List of Product: ' + '</p>'
    response.write(heading1)
    for product in prod_list:
        para1 = '<p>' + str(product.id) + ': ' + str(product.name) + '</p>'
        response.write(para1)
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'prod_list': prod_list, 'testuser': testuser})


def about(request):
    if request.user.is_authenticated:
        testuser = request.user

    else:
        testuser = ""

    if 'about_visits' in request.COOKIES:
        about_visits = int(request.COOKIES['about_visits'])
        about_visits += 1
        response = render(request, 'myapp/about.html', {'about_visits': about_visits, 'testuser': testuser })
        response.set_cookie('about_visits', about_visits, max_age=300)
        return response
    else:
        about_visits = 1
        response = render(request, 'myapp/about.html', {'about_visits': about_visits, 'testuser': testuser})
        response.set_cookie('about_visits', about_visits)
        return response

def detail(request, cat_no):
    if request.user.is_authenticated:
        testuser = request.user

    else:
        testuser = ""



    get_object_or_404(Category, id=cat_no)  # page not found error if cat_no is not found
    try:
        category = Category.objects.get(id=cat_no)  #query to get category name with the id passed in cat_no
        product = Product.objects.filter(category=cat_no) #query to get list of product name with the id passed in cat_no

        response = HttpResponse()  #HTTPResponse
        cat_name = '<p>' + 'Category Name: ' + str(category.name) +'</p>'
        warehouse_name = '<p>' + 'Warehouse Name: ' + str(category.warehouse) + '</p>'

        response.write(cat_name)
        response.write(warehouse_name)

    # loop to print multiple objects of product for every category
        for prod in product:
            product_name = '<p>' + 'Product Name: ' + str(prod.name) + '</p>'
            response.write(product_name)
        #return response
        return render(request, 'myapp/detail.html', {'cat_name': category, 'product': product, 'testuser': testuser})
    except (KeyError, Category.DoesNotExist):
        print("Page not found (404)")


def products(request):
    if request.user.is_authenticated:
        testuser = request.user

    else:
        testuser = ""

    prodlist = Product.objects.all().order_by('id')
    return render(request, 'myapp/products.html', {'prodlist': prodlist, 'testuser': testuser})


def place_order(request):
    if request.user.is_authenticated:
        testuser = request.user

    else:
        testuser = ""

    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_unit <= order.product.stock:
                product = Product.objects.get(name = order.product.name)
                product.stock = product.stock - order.num_unit
                product.save()
                msg = 'Your order has been placed successfully.'
                p = Product()
                p.refill(order.product.name)
                order.save()
            else:
                msg = 'We do not have sufficient stock to fill your order.'
                p = Product()
                p.refill(order.product.name)
                order.save()
            return render(request, 'myapp/order_response.html', {'msg': msg, 'testuser': testuser})
            # else:
            #     msg = "Invalid user, select logged in user to place order"
            #     return render(request, 'myapp/order_response.html', {'msg': msg, 'testuser': testuser})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist, 'testuser': testuser})


def productdetail(request, prod_id):
    if request.user.is_authenticated:
        testuser = request.user

    else:
        testuser = ""

    msg = ''
    prod_list = Product.objects.filter(id=prod_id)
    if request.method == 'POST':
        form = forms.InterestForm(request.POST)
        if form.is_valid():
            if request.POST['interested'] == '1':
                prod = Product.objects.get(id=prod_id)
                prod.interested += 1
                prod.save()
                msg = 'Your interest is updated successfully.'
            else:
                msg = 'Your interest is not updated successfully.'
        return render(request, 'myapp/index.html', {'form': form, 'prod_list': prod_list, 'msg': msg, 'testuser': testuser})
    else:
        form = InterestForm()
        return render(request, 'myapp/productdetail.html', {'form': form, 'prod_list': prod_list, 'msg': msg, 'testuser': testuser})


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cli = Client.objects.get(username=username)
        user = authenticate(request, username=username, password=password)
        request.session.set_expiry(3600)
        if user:
            if user.is_active:
                if 'last_login' in request.session:
                    last_login = request.session.get('last_login')
                else:
                    currentDT = datetime.datetime.now()
                    request.session['last_login'] = str(currentDT.strftime("%d-%m-%Y %H:%M"))
                login(request, user)

                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled')

        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html', {'form': form})

@login_required
def user_logout(request):
    # del request.session['cli']

    # response.delete_cookie('about_visits')
    logout(request)
    response = HttpResponseRedirect(reverse('myapp:index'))
    return response

def myorders(request):
    if request.user.is_authenticated:
        testuser = request.user

        myorder = Order.objects.filter(client__username=request.user)
        return render(request, 'myapp/myorders.html', {'myorder': myorder, 'testuser': testuser})

    else:
        testuser = ""
        message = 'login please'
        return render(request, 'myapp/myorders.html', {'message': message, 'testuser': testuser})



# def forgotpass(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         t_user = Client.objects.get(username=username)
#         password = str(os.urandom(8))
#         t_user.set_password(password)
#         t_user.save()
#         send_mail(
#              'MyApp Password',
#              'Your new Password is:' + password,
#              'Email',
#              [t_user.email],
#          )
#         return render(request, 'myapp/forgotpass.html', {'emailSent': True})
#     else:
#         return render(request, 'myapp/forgotpass.html')
#
#
