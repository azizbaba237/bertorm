from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, ProfilUtilisateur, Panier

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfilUtilisateur.objects.create(utilisateur=instance)
        Panier.objects.create(utilisateur=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    if hasattr(instance, 'panier'):
        instance.panier.save()