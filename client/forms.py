from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'adresse', 'code_postal', 'ville', 'email', 'telephone']
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 2}),
            'telephone': forms.TextInput(attrs={'type': 'tel'}),
        }
