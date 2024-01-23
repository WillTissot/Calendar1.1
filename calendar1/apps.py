import asyncio
from django.apps import AppConfig
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread


class CalendarConfig(AppConfig):
    name = 'calendar1'
    
    def ready(self):
        from .scheduler import scheduledJobs
        scheduledJobs.start()
        #loop = asyncio.new_event_loop()
            #executor = ThreadPoolExecutor(max_workers=4)
        #loop.run_in_executor(executor, scheduledJobs.configureScheduler())
        #asyncio.run(scheduledJobs.configureScheduler())
        #loop.run_until_complete(scheduledJobs.configureScheduler())
        #t = Thread(target=scheduledJobs.configureScheduler())
        #t.start()
        

