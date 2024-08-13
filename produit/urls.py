from django.urls import path
from . import views

urlpatterns = [
    path('categories/create/', views.create_categorie, name='create_categorie'),
    path('categories/list/', views.categorie_list, name='categorie_list'),
    path('create/', views.create_produit, name='create_produit'),
    path('list/', views.produit_list, name='produit_list'),
    path('factures/list/', views.facture_list, name='facture_list'),
    path('factures/create/', views.creer_facture, name='create_facture'),
    path('factures/add_produits/', views.add_produits, name='ajouter_produits'),
    path('factures/generer_pdf/', views.generer_facture_pdf, name='generer_facture_pdf'),
    path('facture/modifier/<int:pk>/', views.modifier_facture, name='modifier_facture'),
    path('facture/imprimer/<int:pk>/', views.generer_facture_pdf, name='imprimer_facture'),
    path('get_produits_by_categorie/', views.get_produits_by_categorie, name='get_produits_by_categorie'),
]
