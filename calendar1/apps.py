import asyncio
from django.apps import AppConfig
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread


class CalendarConfig(AppConfig):
    name = 'calendar1'
    
    def ready(self):
        from .scheduler import scheduledJobs
        #scheduledJobs.stop()
        #scheduledJobs.start()
        #print(12)

        

