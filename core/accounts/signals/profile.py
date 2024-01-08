from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import *

# profile signal handlers
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
        )

@receiver(post_save, sender=Membership)
def create_factor(sender, instance, created, **kwargs):
    if created:
        Factor.objects.create(
            user = instance,
            username = instance.user.username,
            paid = instance.sub.paid,
        )