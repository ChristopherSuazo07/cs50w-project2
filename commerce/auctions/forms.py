from django import forms
from .models import *

class AddProductForms(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['Title', 'Description', 'Final_Price', 'Category', 'Img']
        
     
class AddComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['Comment']
        exclude = ['Author', 'Product',]
        