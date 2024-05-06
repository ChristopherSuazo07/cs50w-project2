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
from django.contrib.auth.decorators import login_required


def index(request):
    
    products = Products.objects.filter(Active=True)
    categories = Categories.objects.all()
    # i = list(products.order_by('?'[:3]))
   
    
    return render(request, "auctions/index.html",{
        'products': products,
        'categories': Categories.objects.all()})

   


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
            new_product = form.save(commit = False) #crea un obj nuevo, sin guardar aun los datos del formulario en la db
            
            new_product.Owner = request.user
            
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
  
    if request.method == 'GET':
        form = AddComment()
        context = {
            'products': products,
            'comments': comments,
            'form':form
        }
        return render(request, "auctions/product.html", context)
    else:
        
        
        form = AddComment(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit = False) #crea un obj nuevo, sin guardar aun los datos del formulario en la db
            
            new_comment.Author = request.user
            new_comment.Product = id
            
            new_comment.save()
            
            context = {
                'form': form,
                'products': products,
                'comments': comments
                }
            return render(request, "auctions/add_product.html",context)  
    
  
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
    return redirect("watchlist")