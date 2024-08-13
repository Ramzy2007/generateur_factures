from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
