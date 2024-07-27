from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Membre, Client,Reservation,Biens_Reservations

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

@receiver(post_save, sender=Profile)
def create_or_update_membership(sender, instance, created, **kwargs):
    if instance.type == 'membre':
        if created:
            Membre.objects.get_or_create(profile=instance)
        else:
            if hasattr(instance, 'membre'):
                instance.membre.save()
            else:
                Membre.objects.get_or_create(profile=instance)

@receiver(post_save, sender=Profile)
def create_or_update_client(sender, instance, created, **kwargs):
    if instance.type == 'client':
        if created:
            Client.objects.get_or_create(profile=instance)
        else:
            if hasattr(instance, 'client'):
                instance.client.save()
            else:
                Client.objects.get_or_create(profile=instance)

@receiver(post_save, sender=Reservation)
def create_or_update_biens_reservations(sender, instance, created, **kwargs):
    if instance.paiement == 'payé':
        print(f"Signal reçu pour réservation {instance.id} avec prix {instance.prix}")  # Log pour débogage

        # Récupérer ou créer l'objet Biens_Reservations associé
        biens_reservation, created = Biens_Reservations.objects.get_or_create(
            reservation=instance
        )

        # Mettre à jour le champ prix et sauvegarder
        biens_reservation.prix = instance.prix if instance.prix is not None and instance.payé_par_pack==0 else 0
        biens_reservation.save()

@receiver(post_save, sender=Reservation)
def update_solde_on_pack_change(sender, instance, **kwargs):
    # Si la réservation est validée et est payée par pack
    if instance.Status == "validé" and instance.payé_par_pack:
        membre = Membre.objects.get(profile=instance.profile)
        # Vérifiez si le membre a un solde suffisant, cela devrait déjà être vérifié avant
        if membre.solde >= instance.duree:
            # Décrémentez le solde du membre par la durée de la réservation
            membre.solde -= instance.duree
            membre.save()
            