from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django import forms
from .models import *
from .models import Products
from .forms import *
import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    
    products = Products.objects.filter(Active=True)
    categories = Categories.objects.all()
    # i = list(products.order_by('?'[:3]))
   
    context = {
        'products': products,
        'categories': Categories.objects.all()
    }
    return render(request, "auctions/index.html",context)

   


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required(login_url="register")
def add_product(request):
    if request.method == "POST":
       form = AddProductForms(request.POST, request.FILES)
       print(f'===================> {form}')
       
       if form.is_valid():
            bid = form.cleaned_data['bid']
            new_product = form.save(commit = False) #crea un obj nuevo, sin guardar aun los datos del formulario en la db
            
            new_product.Owner = request.user
            print("===> value", bid)
            # Add Deals
            bids = Deals(price = bid, user=request.user)
            bids.save()
            
            new_product.price_new_owner = bids
            new_product.initial_price = bid
            new_product.save()
           
            return render(request, "auctions/add_product.html",{
                'form': form
            })  
    form = AddProductForms()
    
     
    return render(request, "auctions/add_product.html",{
        
        'form':form
    })
    
def show_product(request, id):
    products = Products.objects.filter(id = id)
    comments = Comments.objects.filter(Product = id)
    
    print(f'=================>{id}')
    if request.method == 'GET':
        form = AddComment()

        Users = request.user
        if Users.is_authenticated:
            watchlist_bool = WatchList.objects.filter(Person=Users, Product=Products.objects.get(pk=id)).exists()
        
            context = {
                'products': products,
                'comments': comments,
                'form':form,
                'watchlist_bool': watchlist_bool
            }
            return render(request, "auctions/product.html", context)
        
        else:
            context = {
                'products': products,
                'comments': comments,
                'form':form,
                'watchlist_bool': False
            }
            return render(request, "auctions/product.html", context)
    else:
        
        form = AddComment(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit = False) #crea un obj nuevo, sin guardar aun los datos del formulario en la db
            new_comment.Author = request.user
            new_comment.Product = Products.objects.get(pk=id)
            new_comment.save()
            
            context = {
                'form': form,
                'products': products,
                'comments': comments
                }
            return redirect('product', id)
    
  
@login_required(login_url="register")
def watchlist(request):
    
    watchlist = WatchList.objects.filter(Person = request.user)
    
    context ={
        'watchlist': watchlist,
    }
    
    return render(request, 'auctions/watchlist.html', context)
    
def add_watchlist(request, id):
    product = Products.objects.get(id = id) #Select con where id = id 
    watchlist = WatchList(Product= product, Person = request.user)
    watchlist.save()
    print(f"=================>id:{id}<==================")
    return redirect('product', id)

def remove_watchlist(request, id):
    
    removed=WatchList.objects.filter(Product = id)
    print(f'=====================>{removed}')
    removed.delete()
    
    return redirect('product', id)

def add_newpricefor_product(request, id):
    price_new = request.POST.get('offer')
    print("price === > ", price_new)
    product = Products.objects.get(pk=id)
    if float(price_new) > product.price_new_owner.price:
        deal_new = Deals(user=request.user, price=float(price_new))
        deal_new.save()
        product.price_new_owner = deal_new
        product.save()
    else:
        messages.error(request, "The bid has to be higher than the current one")
    return redirect('product', id)

def finishOffer(request,id):
    print("===> Close", id)
    product = Products.objects.get(pk=id)
    product.Active = False
    product.save()
    return redirect('product', id)

def categories(request):
    categories = Categories.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'auctions/categories.html', context)

def category(request, id):
    
    cat = Categories.objects.get(id=id)
    
    products = Products.objects.filter(Category = cat)
    
    products_bool = products.exists()
    
    print(f'=================>{products_bool}\n==================>{products}')
    context ={
        'products': products,
        'products_bool':products_bool
    }
    return render(request, 'auctions/category.html', context)