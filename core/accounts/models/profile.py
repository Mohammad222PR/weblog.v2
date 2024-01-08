from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Skills(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Membership(models.Model):
    MEMBERSHIP_CHOICES = (("Premium", "pre"), ("Free", "free"))
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES, default="Free", max_length=30
    )
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(
        User, related_name="user_membership", on_delete=models.CASCADE, blank=True, null=True
    )
    membership = models.ForeignKey(
        Membership, related_name="user_membership", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserMembership.objects.create(
            user=instance,
            
        )

class Subscription(models.Model):
    user_membership = models.ForeignKey(
        UserMembership, related_name="subscription", on_delete=models.CASCADE
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name="user", on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    age = models.SmallIntegerField(null=True, blank=True)
    bio = models.TextField(max_length=255, blank=True, null=True)
    skills = models.ManyToManyField(Skills, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


# profile signal handlers
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
        )
