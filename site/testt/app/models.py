from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class avions(models.Model):
    immatriculation=models.CharField(max_length=200,unique=True)
    CDN=models.DateField()
    Licence_radio=models.DateField()
    image=models.CharField(max_length=200)
    Assurance=models.DateField()
    Nombres_de_places=models.IntegerField()
    description=models.TextField(max_length=200,null=True)
    status=models.CharField(max_length=15,null=True)
    nom=models.CharField(max_length=15,null=True)
    Rating=models.IntegerField(null=True)
    def __str__(self):
        return self.immatriculation
    
class News(models.Model):
    description = models.TextField()
    image=models.CharField(max_length=200)
    titre=models.CharField(max_length=200,null=True)
    date = models.DateField()

    def __str__(self):
        return self.titre
    
class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('client', 'Client'),
        ('membre', 'Membre'),
    ]
    PILOTE_STATEMENT_CHOICES = [
        ('pilote', 'Pilote'),
        ('non_pilote', 'Non_Pilote'),
    ]
    PILOTE_TYPES_CHOICES = [
        ('pilote_licencié', 'Pilote_Licencié'),
        ('pilote_stagiaire', 'Pilote_Stagiaire'),
    ]
    PILOTE_LICENCE_TYPES_CHOICES = [
        ('instructeur de vol', 'Instructeur de Vol'),
        ('instructeur de sol', 'Instructeur de Sol'),
        ('examinateur de vol', 'Examinateur de Vol'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='client')
    Nom = models.CharField(max_length=20,null=True)
    prenom = models.CharField(max_length=20,null=True)
    CIN = models.CharField(max_length=15,null=True)
    tel = models.CharField(max_length=10,null=True)
    Nationalité = models.CharField(max_length=10,null=True)
    Domicile = models.CharField(max_length=100,null=True)
    Ville = models.CharField(max_length=30,null=True)
    date_naissance = models.DateField(null=True)
    age = models.IntegerField(null=True)
    image = models.CharField(max_length=40,null=True)
    N_carte_stagiaire = models.CharField(max_length=50,null=True)
    carte_validité = models.DateField(max_length=50,null=True)
    status_membre = models.CharField(max_length=10, null=True, blank=True)  # 'active', 'inactive', or null
    etat_pilotage = models.CharField(max_length=80,choices=PILOTE_STATEMENT_CHOICES, null=True, blank=True)  # 'pilote', 'non pilote', or null
    type_pilote = models.CharField(max_length=80, choices=PILOTE_TYPES_CHOICES,null=True, blank=True)  # 'pilote_stagiaire', 'pilote_licencié', or null
    type_pilote_licencie = models.CharField(max_length=80,choices=PILOTE_LICENCE_TYPES_CHOICES, null=True, blank=True)  # 'FI', 'GI', 'FE', or null

    def __str__(self):
        return self.user.username

class Membership(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    date_abonnement = models.DateField(auto_now_add=True,null=True)
    montant_abonnement = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    
    def __str__(self):
        return f'Membership for {self.profile.user.username}'