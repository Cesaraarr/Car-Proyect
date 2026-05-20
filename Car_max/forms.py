from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand', 'model_name', 'year', 'price', 'mileage', 
            'transmission', 'fuel_type', 'engine', 'description', 
            'stock', 'categories'
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }