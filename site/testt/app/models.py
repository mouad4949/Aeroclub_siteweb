from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class avion(models.Model):
    immatriculation = models.CharField(max_length=200, unique=True)
    CDN = models.DateField()
    Licence_radio = models.DateField()
    image = models.CharField(max_length=200)
    Assurance = models.DateField()
    Nombres_de_places = models.IntegerField()
    description = models.TextField(max_length=200, null=True)
    Disponibilité = models.BooleanField(default=1)
    nom = models.CharField(max_length=15, null=True)
    Rating = models.IntegerField(null=True)
    def __str__(self):
        return self.immatriculation
    
class New(models.Model):
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
    def __str__(self):
        return self.user.username
    
class Pack(models.Model):
    
    type=models.CharField(max_length=80)
    prix=models.IntegerField()
    Minutes=models.IntegerField()
    def __str__(self):
        return self.type
        
class Membre(models.Model):
    CHOIX_STATUS = [
        ('active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    pack=models.ForeignKey(Pack, on_delete=models.CASCADE,null=True)
    date_abonnement = models.DateField(auto_now_add=True,null=True)
    date_expiration=models.DateField(null=True)
    montant_abonnement = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    status = models.CharField(max_length=15, choices=CHOIX_STATUS, default='active')
    solde=models.IntegerField(null=True)
    image = models.CharField(max_length=30,null=True)
    
    
    def __str__(self):
        return f'abbonnement pour {self.profile.user.username}'
    

class Client(models.Model):
    
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return  self.profile.user.username
    
class Service(models.Model):
    TYPE_SERVICE= [
        ('vol d initiation', 'VOL D INITATION'),
        ('vol decouverte', 'VOL DECOUVERTE'),
    ]
    type_service=models.CharField(unique=True,choices=TYPE_SERVICE,max_length=80)
    prix=models.IntegerField()

    def __str__(self):
        return self.type_service
    
class Pilotes_Stagiare(models.Model):

    N_carte_stagiaire=models.CharField(unique=True,max_length=80)
    membre = models.OneToOneField(Membre, on_delete=models.CASCADE)
    def __str__(self):
        return self.membre.profile.user.username

class Pilotes_Licencié(models.Model):

    Carte_validité=models.DateField()
    membre = models.OneToOneField(Membre, on_delete=models.CASCADE)
    def __str__(self):
        return self.membre.profile.user.username
    
class Pilotes_Instructeur(models.Model):


    pilote = models.OneToOneField(Pilotes_Licencié, on_delete=models.CASCADE)
    TYPE= [
        ('instructeur de vol', 'Instructeur de Vol'),
        ('instructeur de sol', 'Instructeur de Sol'),
        ('examinateur de vol', 'Examinateur de Vol'),
    ]
    type=models.CharField(unique=True,choices=TYPE,max_length=80,null=True)
    
    Disponibilité=models.BooleanField(default=1)
    
    def __str__(self):
        return self.pilote.membre.profile.user.username
    

class Reservation(models.Model):
    TYPE_RESERVATION = [
        ('vol d initiation', 'VOL D INITIATION'),
        ('vol decouverte', 'VOL DECOUVERTE'),
    ]
    STATUS_CHOIX = [
        ('en attente','EN ATTENTE'),
        ('validé','VALIDÉ'),
    ]
    PAIEMENT_CHOIX= [
        ('payé','PAYÉ'),
        ('impayé','IMPAYÉ'),
        ('annulé','ANNULÉ'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Utilisez ForeignKey au lieu de OneToOneField
    type_reservation=models.CharField(max_length=80,choices=TYPE_RESERVATION)
    prix=models.IntegerField()
    date_depart = models.DateTimeField(null=True)
    date_arrivé =models.DateTimeField(null=True)
    duree = models.IntegerField(null=True)
    date_de_reservation = models.DateTimeField(default=timezone.now)
    Nbrs_places=models.IntegerField(null=True)
    av=models.ForeignKey(avion,on_delete=models.CASCADE,null=True)
    pilote=models.ForeignKey(Pilotes_Instructeur,on_delete=models.CASCADE,null=True)
    Status=models.CharField(max_length=80,choices=STATUS_CHOIX,default="en attente")   
    Sent=models.BooleanField(default=0)
    paiement=models.CharField(max_length=80,choices=PAIEMENT_CHOIX,default="impayé")
    payé_par_pack=models.BooleanField(default=0)

    def __str__(self):
        return self.profile.user.username
    
class Biens_Reservations(models.Model):
    TYPE_CHOIX =[
        ('chéque','Chéque'),
        ('espèce','Espèce'),
        ('Virement','Virement'),
        ('en ligne','En ligne'),
    ]
    reservation=models.OneToOneField(Reservation, on_delete=models.CASCADE)
    type_paiement=models.CharField(max_length=80,null=True,choices=TYPE_CHOIX)
    prix=models.IntegerField(null=True)
    libellé=models.TextField(null=True)
    
    def __str__(self):
        return f"{self.reservation.profile.prenom}{self.reservation.profile.Nom}"
    
