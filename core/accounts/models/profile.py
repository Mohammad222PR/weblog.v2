from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


User = get_user_model()


class Skills(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    name = models.CharField(max_length=200)
    paid = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.name
    
    def is_expired(self):
        return self.time < timezone.now()
    

class Membership(models.Model):
    user = models.OneToOneField(User, blank=True, null=True,on_delete=models.CASCADE)
    sub = models.OneToOneField(Subscription, on_delete=models.CASCADE)
    
class Factor(models.Model):
    user = models.OneToOneField(User, blank=True, null=True,on_delete=models.CASCADE)
    sub = models.OneToOneField(Subscription, on_delete=models.CASCADE)
    paid = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)



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


