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
    calCourseEvents = Event.objects.filter(calendarSeminar__isnull=True)
    calSeminarEvents = Event.objects.filter(calendarCourse__isnull=True)
    context = {
        'calCourseEvents': calCourseEvents,
        'calSeminarEvents' : calSeminarEvents
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

    if request.method == 'POST':
        event.delete()
        return redirect('event:event_list')

    context = {
        'event': event
    }
    return render(request, 'event_delete.html', context)

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
