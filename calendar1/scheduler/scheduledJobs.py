import asyncio
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution

def tick():
    print('Tick! The time is: %s' % datetime.now())

def start():
    # Your command logic goes here
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(tick, 'interval', seconds=5, name='clean_accounts', jobstore='default')
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...")
