from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Categories(models.Model):
    Category = models.CharField(max_length = 64)
    
    def __str__(self):
        return f"{self.Category}"


class Deals(models.Model):
    price = models.FloatField()
    user = models.ForeignKey(User, related_name="DealProducts" ,on_delete=models.CASCADE, null=True, blank=True)
       
    def __str__(self):
        return f"price {self.price} user {self.user}"

class Products(models.Model):
    Owner = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'owner', blank = True, null= True)
    Title = models.CharField(max_length=64)
    Description = models.TextField()
    Active = models.BooleanField(default= True)
    Category = models.ForeignKey(Categories, on_delete= models.CASCADE, related_name= "category")
    Img = models.ImageField(upload_to='image/Project2/', blank=True, null=True)
    initial_price = models.FloatField()
    price_new_owner = models.ForeignKey(Deals, on_delete=models.CASCADE)
  
    def __str__(self):
        return f" Id:{self.id} Product:{self.Title} Description: {self.Description} Price{self.initial_price} Active:{self.Active} Category:{self.Category}"

class Comments(models.Model):
    Author = models.ForeignKey(User, on_delete= models.CASCADE, blank = True, null = True, related_name= "author_comment")
    Comment = models.TextField()
    Product = models.ForeignKey(Products, on_delete= models.CASCADE, blank = True, null = True, related_name= "product_comment")
    
class WatchList(models.Model):
    Product = models.ForeignKey(Products, on_delete = models.CASCADE, blank= True, related_name = 'product')
    Person = models.ForeignKey(User, on_delete= models.CASCADE, blank=True, related_name = 'person')
    
    def __str__(self):
        return f'{self.Product}{self.Person}'
