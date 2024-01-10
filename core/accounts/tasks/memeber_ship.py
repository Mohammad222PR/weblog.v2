# tasks.py
from celery import shared_task
from datetime import datetime
from accounts.models import *
from django_celery_beat.models import PeriodicTask


@shared_task
def remove_expired_subscriptions():
    """celery task for membership"""
    membership = Membership.objects.all()
    if membership.end_date <= datetime.now():
        for member in membership:
            member.delete()


@shared_task
def clean_up_completed_tasks():
    tasks = PeriodicTask.objects.filter(enabled=False)
    for task in tasks:
        task.delete()
    print("clean_up_completed_tasks completed")
