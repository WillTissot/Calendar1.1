from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from course.models import Course

from event.forms import EventForm
from .models import Event, Student, Professor
from django.contrib.auth.decorators import user_passes_test

@login_required
def event_list(request):
    # Get the logged-in user
    user = request.user

    # Check if the user is a student
    if hasattr(user, 'student'):
        # If the user is a student, get all events associated with their student object
        events = Event.objects.filter(student=user.student)

    # Otherwise, check if the user is a professor
    elif hasattr(user, 'professor'):
        # If the user is a professor, get all events associated with their professor object
        events = Event.objects.filter(professor=user.professor)

    # If the user is not a student or a professor, return an empty list of events
    else:
        events = []

    # Render the event list template with the events
    return render(request, 'my_event_list.html', {'events': events})

@login_required
def dashboard(request):
    student = request.user.student # assuming your User model has a OneToOneField to a Student model
    
    context = {
        'student': student,
    }
    
    return render(request, 'dashboard.html', context)

def homepage(request):
    return render(request, 'homepage.html')


@user_passes_test(lambda u: u.is_superuser)
def adminpage(request):
    return render(request, 'adminpage.html')

def sec_event_list(request):
    events = Event.objects.all()
    context = {
        'events': events
    }
    return render(request, 'event_list.html', context)

def get_students(request, ev_id):
    event = Event.objects.get(id=ev_id)
    student_ids = [event.student_id]
    students = Student.objects.filter(id__in=student_ids)

    context = {
        'students': students
    }
    return render(request, 'student_list.html', context)

def event_detail(request, ev_id):
    # Retrieve the student object with the provided id
    event = get_object_or_404(Event, id=ev_id)

    # Render the student detail template with the student object as context
    return render(request, 'event_detail.html', {'event': event})


def event_update(request, ev_id):
    event = get_object_or_404(Event, id=ev_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event:event_detail', cou_id=ev_id)
    else:
        form = EventForm(instance=event)
    return render(request, 'event_update.html', {'form': form})

def event_delete(request, ev_id):
    event = get_object_or_404(Event, id=ev_id)

    if request.method == 'POST':
        event.delete()
        return redirect('event:event_list')

    context = {
        'event': event
    }
    return render(request, 'event_delete.html', context)


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

