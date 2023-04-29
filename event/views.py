from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Event, Student, Professor

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
    return render(request, 'events_list.html', {'events': events})

@login_required
def dashboard(request):
    student = request.user.student # assuming your User model has a OneToOneField to a Student model
    
    context = {
        'student': student,
    }
    
    return render(request, 'dashboard.html', context)
