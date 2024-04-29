from django import forms
from .models import Products

class AddProductForms(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['Title', 'Description', 'Price', 'Category', 'Img']
        
     
