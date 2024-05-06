from django import forms
from .models import *

class AddProductForms(forms.ModelForm):
    bid = forms.FloatField(label='price', required=True)
    class Meta:
        model = Products
        fields = ['Title', 'Description', 'Category', 'Img']
        
     
class AddComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['Comment']
        
        