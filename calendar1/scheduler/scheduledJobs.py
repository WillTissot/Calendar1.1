import asyncio
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from datetime import datetime, timedelta
from event.models import Event
from student.models import EnrolledStudentsOnCalendarCourse

#existingJob = False

def sendEmails(studentMails, lesson, roomnumber, starttime):
    #print('Tick! The time is: %s' % datetime.now())
    print("sends email")
    send_mail(
        subject='Class Reminder',
        message=f'Your class {lesson} is about to start at {starttime} at {roomnumber}',
        from_email='shopwaresync@gmail.com',
        recipient_list=studentMails
    )

def MailBackgroundService():
    print("Background service starts!")
    current_datetime = datetime.now()
    # Calculate 30 minutes before the current time
    start_time_in_30_minutes = current_datetime + timedelta(minutes=30)
    print(start_time_in_30_minutes)
    # Filter events that are scheduled for today and within the next 30 minutes before the start time
    events_in_30_minutes = Event.objects.filter(
        date=current_datetime.date(),  # Filter by today's date
        calendarCourse__start_time__gte=current_datetime.time(),  # Filter by events starting now or later
        calendarCourse__start_time__lt=start_time_in_30_minutes.time(),  # Filter by events starting in the next 30 minutes
    )
    #print(events_in_30_minutes)
    for event in events_in_30_minutes:
        #event = get_object_or_404(Event, id=ev_id)
        print("inside loop")
        calCourse = event.calendarCourse
        enrolled_students = EnrolledStudentsOnCalendarCourse.objects.filter(calendarCourse=calCourse)
        student_mails = enrolled_students.values_list('student__user__email', flat=True)
        sendEmails(student_mails, calCourse.course.title, calCourse.room_number, calCourse.start_time)

def start():
    # Your command logic goes here
    scheduler = BackgroundScheduler()
    # global existingJob
    # if not existingJob:     
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(MailBackgroundService, 'interval', minutes=1, id='Mail1')
    register_events(scheduler)
    scheduler.start()
    #existingJob = true
    print("Scheduler started...")

def stop():
    scheduler = BackgroundScheduler()
    #scheduler.remove_job('Mail1')
