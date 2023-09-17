from django import forms
from .models import EventPrice

class EventPriceForm(forms.ModelForm):
    eventid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),label="Title ",required=True)
    price = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}),label="Event Price ",required=True)
    class Meta:
        model = EventPrice 
        fields = ['eventid','title','price']
