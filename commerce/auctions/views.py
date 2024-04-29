from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from .models import *
from .models import Products
from .forms import *
import random



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
    

def add_product(request):
    if request.method == "POST":
       form = AddProductForms(request.POST, request.FILES)
       print(f'===================> {form}')
       
       if form.is_valid():
            new_product = form.save(commit = False) #crea un obj nuevo, sin guardar aun los datos del formulario en la db
            
            new_product.Owner = request.user
            print(f'===================>{new_product}')
            new_product.save()
      
            return render(request, "auctions/add_product.html",{
                'form': form
            })    
    form = AddProductForms()
    
    return render(request, "auctions/add_product.html",{
        
        'form':form
    })
    
def show_product(request, id):
    products = Products.objects.filter(id=id)
    context = {
        'product': products,
    }
    return render(request, "auctions/product.html", context)
