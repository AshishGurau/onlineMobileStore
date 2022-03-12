from django import forms
from django.forms import ModelForm
from .models import Sale

class SaleForm(ModelForm):
    class Meta:
        model = Sale
        fields = [
            'image', 
            'p_name',
            'price',
            ]