from django.db import models
from client.models import Client
from django.utils import timezone

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    marque = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    tva = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.nom} ({self.marque})"

class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    produits = models.ManyToManyField(Produit, through='DetailFacture')
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Facture {self.id} - {self.client.nom}"

class DetailFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix = models.DecimalField(max_digits=10, decimal_places=2)

