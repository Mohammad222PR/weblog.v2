# tasks.py
from celery import shared_task
from datetime import datetime
from accounts.models import *

@shared_task
def remove_expired_subscriptions():
    now = datetime.now()
    expired_subscriptions = Membership.objects.filter(time__lt=now)

    for membership in expired_subscriptions:
        membership.delete()
