from django import forms
from .models import Categorie, Produit, Facture, DetailFacture

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'marque', 'reference', 'categorie', 'description', 'prix', 'tva']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['client']

class DetailFactureForm(forms.ModelForm):
    class Meta:
        model = DetailFacture
        fields = ['produit', 'quantite', 'prix']
