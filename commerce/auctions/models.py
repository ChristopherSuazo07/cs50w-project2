from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Categories(models.Model):
    Category = models.CharField(max_length = 64)
    
    def __str__(self):
        return f"{self.Category}"
    
class Products(models.Model):
    Owner = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'owner', blank = True, null= True)
    Title = models.CharField(max_length=64)
    Description = models.TextField()
    Final_Price = models.FloatField(default = 0)
    Price = models.FloatField()
    Active = models.BooleanField(default= True)
    Category = models.ForeignKey(Categories, on_delete= models.CASCADE, related_name= "category")
    Img = models.ImageField(upload_to='image/Project2/', blank=True, null=True)
    
    def __str__(self):
        return f"Product:{self.Title} Description: {self.Description} Price{self.Price} Active:{self.Active} Category:{self.Category} Final_Price:{self.Final_Price}"

class Comments(models.Model):
    Author = models.ForeignKey(User, on_delete= models.CASCADE, blank = True, null = True, related_name= "author_comment")
    Comment = models.TextField()
    Prouct = models.ForeignKey(Products, on_delete= models.CASCADE, blank = True, null = True, related_name= "product_comment")

class Deals(models.Model):
    Biggest_bid = models.FloatField()
    Top_bidder = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "Top_bidder" )
    
    def __str__(self):
        return f"Top Bidder: {self.Top_bidder} Biggest Bidder:{self.Biggest_bid}"
    
class WatchList(models.Model):
    Product = models.ForeignKey(Products, on_delete = models.CASCADE, blank= True, related_name = 'product')
    Person = models.ForeignKey(User, on_delete= models.CASCADE, blank=True, related_name = 'person')
    
    def __str__(self):
        return f'{self.Product}{self.Person}'
