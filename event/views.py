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

def get_events(request):
    user= request.user

    if hasattr(request.user, 'student'):
        coursesEvents = Event.objects.filter(calendarCourse__enrolledstudentsoncalendarcourse__student=user.student).order_by('calendarCourse__start_time')
        seminarsEvents = Event.objects.filter(calendarSeminar__enrolledstudenttocalendarseminars__students=user.student)
        dissertationEvent = Event.objects.get(calendarDissertation__dissertation__student=user.student)
    if hasattr(request.user, 'professor'):
        coursesEvents = Event.objects.filter(calendarCourse__course__professor=user.professor)
        dissertationEventsAsSupervisor = Event.objects.filter(calendarDissertation__dissertation__supervisor=user.professor)
        dissertationEventsAsSBoardMember = Event.objects.filter(calendarDissertation__dissertation__board=user.professor)
    data = []
    if hasattr(request.user, 'student'):
        for coursesEvent in coursesEvents:
            data.append({
                'title': coursesEvent.calendarCourse.course.title + ' ' + coursesEvent.calendarCourse.start_time.strftime('%H:%M') + ' - ' + coursesEvent.calendarCourse.end_time.strftime('%H:%M'),
                'start': coursesEvent.date.isoformat(),
                'end': coursesEvent.date.isoformat()  
            })
        for seminarsEvent in seminarsEvents:
            data.append({
                'title': seminarsEvent.calendarSeminar.seminar.title,
                'start': seminarsEvent.date.isoformat(),
                'end': seminarsEvent.date.isoformat()  
            })
        if dissertationEvent is not None:
            data.append({
                'title': dissertationEvent.calendarDissertation.dissertation.title,
                'start': dissertationEvent.date.isoformat(),
                'end': dissertationEvent.date.isoformat()  
            })
        return JsonResponse(data, safe=False)
    if hasattr(request.user, 'professor'):
        for coursesEvent in coursesEvents:
            data.append({
                'title': coursesEvent.calendarCourse.course.title + ' ' + coursesEvent.calendarCourse.start_time.strftime('%H:%M') + ' - ' + coursesEvent.calendarCourse.end_time.strftime('%H:%M'),
                'start': coursesEvent.date.isoformat(),
                'end': coursesEvent.date.isoformat()  
            })
        for eventAsSupervisor in dissertationEventsAsSupervisor:
            data.append({
                'title': eventAsSupervisor.calendarSeminar.seminar.title,
                'start': eventAsSupervisor.date.isoformat(),
                'end': eventAsSupervisor.date.isoformat()  
            })
        for eventAsBoardMember in dissertationEventsAsSBoardMember:
            data.append({
                'title': eventAsBoardMember.calendarSeminar.seminar.title,
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
        'event' : event
    }
    return render(request, 'student_popup.html', context)

@user_passes_test(lambda u: u.is_superuser)
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

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event:event_detail', ev_id=ev_id)
    else:
        form = EventForm(instance=event)
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
