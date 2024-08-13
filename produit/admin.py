from django.contrib import admin
from .models import Categorie, Facture, Produit, DetailFacture

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'marque', 'reference', 'categorie', 'description', 'prix', 'tva')

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'get_produits')

    def get_produits(self, obj):
        return ", ".join([f"{detail.produit.nom} (x{detail.quantite})" for detail in DetailFacture.objects.filter(facture=obj)])
    get_produits.short_description = 'Produits'

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
