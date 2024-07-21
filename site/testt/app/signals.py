from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Membre, Client

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
