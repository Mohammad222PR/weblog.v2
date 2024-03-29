from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta

User = get_user_model()


class Skills(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    name = models.CharField(max_length=200)
    paid = models.IntegerField()
    time = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='membership')
    sub = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now=True)


@receiver(post_save, sender=Membership)
def set_end_date(sender, created, instance, **kwargs):
    if created:
        Membership.objects.update(
            end_date=instance.start_date + timedelta(days=int(instance.sub.time))
        )


class Factor(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    sub = models.CharField(max_length=200)
    price = models.IntegerField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=Membership)
def create_factor_membership(sender, created, instance, **kwargs):
    if created:
        Factor.objects.create(
            user=instance.user,
            sub=instance.sub.name,
            start_date=instance.start_date,
            price=instance.sub.paid
        )
    Factor.objects.update(
        end_date=instance.start_date + timedelta(days=int(instance.sub.time))
    )


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
