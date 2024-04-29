from django.contrib import admin
from .models import Categories, Products, Comments, Deals, WatchList
# Register your models here.

admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Comments)
admin.site.register(Deals)
admin.site.register(WatchList)