from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from course.models import Course, CalendarCourse
from datetime import date, timedelta, datetime
from event.forms import EventForm
from .models import Event, Student, Professor
from student.models import EnrolledStudentsOnCourse, EnrolledStudentsOnCalendarCourse
from django.contrib.auth.decorators import user_passes_test

@login_required
def event_list(request):
    user= request.user
    if hasattr(user, 'student'):
        events = Event.objects.filter(calendarCourse__enrolledstudentsoncalendarcourse__student=user.student).distinct()
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
    events = Event.objects.all()
    context = {
        'events': events
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
    
    redirect('course:calendarcourse_list')

def create_change_request(request):
    change = x 
