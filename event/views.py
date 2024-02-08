from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from course.models import Course, CalendarCourse
from datetime import date, timedelta, datetime
from event.forms import EventForm
from .models import Event, Student, Professor, Change
from student.models import EnrolledStudentsOnCourse, EnrolledStudentsOnCalendarCourse
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django import template
from django.contrib.auth.models import User
from django.http import JsonResponse
from seminar.models import EnrolledStudentToCalendarSeminars, CalendarSeminar
from dissertation.models import Dissertation, CalendarDissertation
from course.models import CalendarCourse
from django.db.models import Max, F
from django.core.mail import send_mail

@login_required
def get_events(request):
    user= request.user

    if hasattr(request.user, 'student'):
        coursesEvents = Event.objects.filter(calendarCourse__enrolledstudentsoncalendarcourse__student=user.student).order_by('calendarCourse__start_time')
        seminarsEvents = Event.objects.filter(calendarSeminar__enrolledstudenttocalendarseminars__students=user.student).order_by('calendarSeminar__start_time')
        try:
            dissertationEvent = Event.objects.get(calendarDissertation__dissertation__student=user.student)
        except:
            dissertationEvent = None
    if hasattr(request.user, 'professor'):
        coursesEvents = Event.objects.filter(calendarCourse__course__professor=user.professor).order_by('calendarCourse__start_time')
        dissertationEventsAsSupervisor = Event.objects.filter(calendarDissertation__dissertation__supervisor=user.professor)
        dissertationEventsAsSBoardMember = Event.objects.filter(calendarDissertation__dissertation__board=user.professor)
    data = []
    if hasattr(request.user, 'student'):
        for coursesEvent in coursesEvents:
            lastChange = coursesEvent.changes.filter(is_approved=True, is_pending=False).order_by('-date_created').first()
            if lastChange is None:
                data.append({
                    'title': coursesEvent.calendarCourse.course.title + ' ' + coursesEvent.calendarCourse.start_time.strftime('%H:%M') + ' - ' + coursesEvent.calendarCourse.end_time.strftime('%H:%M'),
                    'start': coursesEvent.date.isoformat(),
                    'end': coursesEvent.date.isoformat()  
                })
            else:
                data.append({
                    'title': coursesEvent.calendarCourse.course.title + ' ' + lastChange.start_time.strftime('%H:%M') + ' - ' + lastChange.end_time.strftime('%H:%M'),
                    'start': lastChange.date.isoformat(),
                    'end': lastChange.date.isoformat()  
                })
        for seminarsEvent in seminarsEvents:
            lastChange = coursesEvent.changes.filter(is_approved=True, is_pending=False).order_by('-date_created').first()
            data.append({
                'title': seminarsEvent.calendarSeminar.seminar.title + ' ' + seminarsEvent.calendarSeminar.start_time.strftime('%H:%M') + ' - ' + seminarsEvent.calendarSeminar.end_time.strftime('%H:%M'),
                'start': seminarsEvent.date.isoformat(),
                'end': seminarsEvent.date.isoformat()  
            })
        if dissertationEvent is not None:
            data.append({
                'title': dissertationEvent.calendarDissertation.dissertation.title + ' ' + dissertationEvent.calendarDissertation.start_time.strftime('%H:%M') + ' - ' + dissertationEvent.calendarDissertation.end_time.strftime('%H:%M'),
                'start': dissertationEvent.date.isoformat(),
                'end': dissertationEvent.date.isoformat()  
            })
        return JsonResponse(data, safe=False)
    if hasattr(request.user, 'professor'):
        for coursesEvent in coursesEvents:
            lastChange = coursesEvent.changes.filter(is_approved=True, is_pending=False).order_by('-date_created').first()
            if lastChange is None:
                data.append({
                    'title': coursesEvent.calendarCourse.course.title + ' ' + coursesEvent.calendarCourse.start_time.strftime('%H:%M') + ' - ' + coursesEvent.calendarCourse.end_time.strftime('%H:%M'),
                    'start': coursesEvent.date.isoformat(),
                    'end': coursesEvent.date.isoformat()  
                })
            else:
                data.append({
                    'title': coursesEvent.calendarCourse.course.title + ' ' + lastChange.start_time.strftime('%H:%M') + ' - ' + lastChange.end_time.strftime('%H:%M'),
                    'start': lastChange.date.isoformat(),
                    'end': lastChange.date.isoformat()  
                })
        for eventAsSupervisor in dissertationEventsAsSupervisor:
            data.append({
                'title': eventAsSupervisor.calendarDissertation.dissertation.title + ' ' + eventAsSupervisor.calendarDissertation.start_time.strftime('%H:%M') + ' - ' + eventAsSupervisor.calendarDissertation.end_time.strftime('%H:%M'),
                'start': eventAsSupervisor.date.isoformat(),
                'end': eventAsSupervisor.date.isoformat()  
            })
        for eventAsBoardMember in dissertationEventsAsSBoardMember:
            data.append({
                'title': eventAsBoardMember.calendarDissertation.dissertation.title + ' ' + eventAsBoardMember.calendarDissertation.start_time.strftime('%H:%M') + ' - ' + eventAsBoardMember.calendarDissertation.end_time.strftime('%H:%M'),
                'start': eventAsBoardMember.date.isoformat(),
                'end': eventAsBoardMember.date.isoformat()  
            })
        return JsonResponse(data, safe=False)

def calendar_view(request):
    return render(request, 'calendarFormat.html')


@login_required
def event_list(request):
    user= request.user
    if hasattr(user, 'student'):
        events = Event.objects.filter(calendarCourse__enrolledstudentsoncalendarcourse__student=user.student)
    elif hasattr(user, 'professor'):
        events = Event.objects.filter(calendarCourse__course__professor__user_id=user.id)
    else:
        events = []

    return render(request, 'my_event_list.html', {'events': events})

@login_required
def dashboard(request):
    user= request.user

    if hasattr(user, 'student'):
        student = request.user.student 
        context = {
            'student': student,
        }
    elif hasattr(user, 'professor'):
        professor = request.user.professor 
        context = {
            'professor': professor,
        }
    return render(request, 'dashboard.html', context)

def homepage(request):
    return render(request, 'homepage.html')


@user_passes_test(lambda u: u.is_superuser)
def adminpage(request):
    return render(request, 'adminpage.html')

@user_passes_test(lambda u: u.is_superuser)
def sec_event_list(request):
    calCourseEvents = Event.objects.filter(calendarSeminar__isnull=True, calendarDissertation__isnull=True)
    latest_changes = Change.objects.filter(event__in=calCourseEvents).values('event').annotate(latest_change=Max('date_created'))
    calCourseEvents_with_latest_change = calCourseEvents.filter(id__in=latest_changes.values('event'))
    calCourseEvents_approved = calCourseEvents_with_latest_change.filter(changes__is_approved=True)

    calSeminarEvents = Event.objects.filter(calendarCourse__isnull=True, calendarDissertation__isnull=True)
    calDissertationEvents = Event.objects.filter(calendarSeminar__isnull=True, calendarCourse__isnull=True)
    context = {
        'calCourseEvents': calCourseEvents,
        'calSeminarEvents' : calSeminarEvents,
        'calDissertationEvents' : calDissertationEvents
    }
    return render(request, 'event_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def get_students(request, ev_id):
    event = get_object_or_404(Event, id=ev_id)
    calCourse = event.calendarCourse
    enrolled_students = EnrolledStudentsOnCalendarCourse.objects.filter(calendarCourse=calCourse)
    student_ids = enrolled_students.values_list('student_id', flat=True)
    students = Student.objects.filter(id__in=student_ids)

    context = {
        'students': students,
        'event' : event,
        'showButton' : False
    }
    return render(request, 'student_popup.html', context)


def get_changes(request, ev_id):
    event = get_object_or_404(Event, id=ev_id)
    context = {
        'event': event
    }
    return render(request, 'changes_popup.html', context)

@user_passes_test(lambda u: u.is_superuser)
def event_detail(request, ev_id):
    # Retrieve the student object with the provided id
    event = get_object_or_404(Event, id=ev_id)

    # Render the student detail template with the student object as context
    return render(request, 'event_detail.html', {'event': event})

@user_passes_test(lambda u: u.is_superuser)
def event_update(request, ev_id):
    event = get_object_or_404(Event, id=ev_id)
    eventProper = event.changes.filter(is_approved=True, is_pending=False).order_by('-date_created').first()
    calCourse = event.calendarCourse
    calSeminar = event.calendarSeminar
    calDissertation = event.calendarDissertation
    if request.method == 'POST':
        change = Change(
            date=request.POST['date'],
            is_online= True if request.POST['is_online'] == 'on' else False,
            start_time=request.POST['start_time'],
            end_time=request.POST['end_time'],
            room_number=request.POST['room_number'],
            is_approved=True,
            date_created=datetime.now()
        )
        change.save()
        event.changes.add(change)
        event.save()
        # form = EventForm(request.POST, instance=event, calendarCourse=calCourse, calendarSeminar = calSeminar, calendarDissertation = calDissertation)
        # if form.is_valid():
        #     form.save()
        return redirect('event:event_detail', ev_id=ev_id)
    else:
        form = EventForm(instance=event, calendarCourse=calCourse, calendarSeminar = calSeminar, calendarDissertation = calDissertation)
    return render(request, 'event_update.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def event_delete(request, ev_id):
    event = get_object_or_404(Event, id=ev_id)

    try:
        if request.method == 'POST':
            if event.calendarSeminar:
                calSeminar  = event.calendarSeminar
                calSeminar.onCalendar = False
                calSeminar.save()
            event.delete()
            return redirect('event:sec_event_list')

        context = {
            'event': event
        }
        return render(request, 'event_delete.html', context)
    except Exception as e:
        context = {
            'event': event,
            'message' : 'Event can not be deleted. People are participating in.'
        }
        return render(request, 'event_detail.html', context)

@user_passes_test(lambda u: u.is_superuser)
def event_create(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = EventForm(request.POST)

        if form.is_valid():
            # create a new student object from the form data
            event = form.save()

            # redirect to the student detail page for the new student object
            return redirect('event:event_detail', ev_id=event.pk)
        else:
            # If the form is not valid, print the form errors for debugging
            print(form.errors)
    else:
        # display a blank form
        form = EventForm()

    # render the create student form template with the form instance
    courses = Course.objects.all()
    professors = Professor.objects.all()
    context = {
                'form': form,
                'departments': courses,
                'professors' : professors
            }
    return render(request, 'event_create.html', context)

@user_passes_test(lambda u: u.is_superuser)
def create_calendar_event(request, cal_id):
    calCourse = get_object_or_404(CalendarCourse, id = cal_id )
    if not calCourse.onCalendar:
        calSemStartDate = calCourse.calendarSemester.startDate
        day = calCourse.day
        calSemEndDate = calCourse.calendarSemester.endDate
        currentDate = datetime.now().date()

        if currentDate < calSemStartDate:
            timed = timedelta(days=(day - calSemStartDate.isoweekday() + 7) % 7)
            nextEventsStartDate = calSemStartDate + timed
        else:
            nextEventsStartDate = currentDate + timedelta(days=(day - currentDate.isoweekday() + 7) % 7)

        while nextEventsStartDate <= calSemEndDate:
            newEvent = Event(
            calendarCourse=calCourse,
            created_at= datetime.now(),
            date = nextEventsStartDate
            )
            newEvent.save()
            nextEventsStartDate += timedelta(days=7)

        calCourse.onCalendar = True
        calCourse.save()
    
    return redirect('course:calendarcourse_list')

@user_passes_test(lambda u: u.is_superuser)
def get_all_requests(request):
    if request.method == 'GET':
        events = Event.objects.annotate(num_changes=Count('changes')).filter(num_changes__gt=0)
        context = {
            'events' : events
        }
        return render(request, 'my_event_list.html', context)
    elif request.method == 'POST':
        changeId = request.POST.get('changeId')
        action = request.POST.get('action')
        eventId = request.POST.get('eventId')
        event = get_object_or_404(Event, id = eventId)
        change = get_object_or_404(Change, id = changeId)
        if action == 'Approve':
            change.is_approved = True
            change.is_pending = False
        elif action == 'Reject':
            change.is_pending = False
            change.is_approved = False
        change.save()
        context = {
            'event' : event
        }
        return render(request, 'changes_popup.html', context)


@user_passes_test(lambda u: u.is_superuser)
def validate_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save()
        return redirect('event:users_approve')
    else:
        users = User.objects.filter(is_active = False)
        context = {
            'users' : users
        }
        return render(request, 'users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def event_create(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = EventForm(request.POST)

        if form.is_valid():
            # create a new student object from the form data
            event = form.save()

            # redirect to the student detail page for the new student object
            return redirect('event:event_detail', ev_id=event.pk)
        else:
            # If the form is not valid, print the form errors for debugging
            print(form.errors)
    else:
        # display a blank form
        form = EventForm()

    # render the create student form template with the form instance
    courses = Course.objects.all()
    professors = Professor.objects.all()
    context = {
                'form': form,
                'departments': courses,
                'professors' : professors
            }
    return render(request, 'event_create.html', context)


@login_required
def see_my_profile(request):
    user = request.user
    if hasattr(user, 'student'):
        return redirect('student:student_detail', det_id=user.student.pk)
    else:
        return redirect('professor:professor_detail', prof_id=user.professor.pk)


@user_passes_test(lambda u: u.is_superuser)
def delete_calendar_course_event(request, cal_id):
    calCourse = get_object_or_404(CalendarCourse, id = cal_id )
    if  calCourse.onCalendar:
        events = Event.objects.filter(calendarCourse = calCourse)
        calCourse.onCalendar = False
        calCourse.save()
        for event in events:
            event.delete()
    
    return redirect('course:calendarcourse_list')

@user_passes_test(lambda u: u.is_superuser)
def delete_calendar_seminar_event(request, sem_id):
    calSeminar = get_object_or_404(CalendarSeminar, id = sem_id )
    if  calSeminar.onCalendar:
        events = Event.objects.filter(calendarSeminar = calSeminar)
        calSeminar.onCalendar = False
        calSeminar.save()
        for event in events:
            event.delete()
    
    return redirect('seminar:calendarseminar_list')


@user_passes_test(lambda u: u.is_superuser)
def delete_calendar_dissertation_event(request, dis_id):
    calDissertation = get_object_or_404(CalendarDissertation, id = dis_id )
    if  calDissertation.onCalendar:
        events = Event.objects.filter(calendarDissertation = calDissertation)
        calDissertation.onCalendar = False
        calDissertation.save()
        for event in events:
            event.delete()
    
    return redirect('dissertation:calendardissertation_list')

def send_mail_changes(request, ev_id):
    event = get_object_or_404(Event, id=ev_id)
    calCourse = event.calendarCourse
    professor = calCourse.course.professor
    enrolled_students = EnrolledStudentsOnCalendarCourse.objects.filter(calendarCourse=calCourse)
    emails_to_send = list(enrolled_students.values_list('student__user__email', flat=True))
    emails_to_send.append(professor.user.email)
    last = event.changes.filter(is_approved=True, is_pending=False).order_by('-date_created').first()
    send_mail(
        subject='Your class information has changed!',
        message=f'Your class {calCourse.course.title} is now on {last.date}, {last.start_time} - {last.end_time} at {last.room_number}',
        from_email='shopwaresync@gmail.com',
        recipient_list=emails_to_send
    )
    return redirect('event:get_all_requests')




