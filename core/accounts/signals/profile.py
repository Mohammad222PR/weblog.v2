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
