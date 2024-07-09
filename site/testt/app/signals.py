from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Membership

@receiver(post_save, sender=User)
def create_profile_and_membership(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Profile)
def create_or_update_membership(sender, instance, created, **kwargs):
    if instance.type == 'membre':  # Vérifiez si le type est membre
        if created:
            Membership.objects.create(profile=instance)
        else:
            if not hasattr(instance, 'membership'):
                Membership.objects.create(profile=instance)
            else:
                instance.membership.save()