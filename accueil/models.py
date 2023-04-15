from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Client(models.Model):
    nom = models.CharField(max_length=200, null=True, blank=True)
    prenom = models.CharField(max_length=200, null=True, blank=True)
    dnaiss = models.DateField(null=True, blank=True)
    residence = models.CharField(max_length=200, null=True, blank=True)
    nationalite = models.CharField(max_length=200, null=True, blank=True)
    sexe = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to='./image/', null=True, blank=True)
    numero_passeport = models.CharField(max_length=200, null=True, blank=True)
    date_expiration_passeport = models.DateField(null=True, blank=True)
    date_created = models.DateField( auto_now_add=True, null=True, blank=True)
    save_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Service(models.Model):
    libelle = models.CharField(max_length=200, null=True, blank=True)
    nombre_jours = models.IntegerField(null=True, blank=True)
    montant = models.FloatField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.libelle}"


class Appartenir(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    destination = models.CharField(max_length=200, null=True, blank=True)
    quantite = models.IntegerField(null=True, blank=True)
    total_unitaire = models.FloatField(max_length=200, null=True, blank=True)
    date_debut = models.DateTimeField(null=True, blank=True)
    date_expiration = models.DateTimeField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.client}/{self.service}"
