from django.shortcuts import get_object_or_404, redirect, render, reverse
from course.models import Department, CalendarCourse
from course.forms import CalendarCourseProfForm
from professor.forms import ProfessorForm
from event.models import Event, Change
from professor.models import Professor
from datetime import datetime
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def professor_list(request):
    professors = Professor.objects.all()
    context = {
        'professors': professors
    }
    return render(request, 'professor_list.html', context)

def professor_detail(request, prof_id):
    # Retrieve the student object with the provided id
    professor = get_object_or_404(Professor, id=prof_id)

    # Render the student detail template with the student object as context
    return render(request, 'professor_detail.html', {'professor': professor})

def professor_update(request, prof_id):
    professor = get_object_or_404(Professor, id=prof_id)

    if request.method == 'POST':
        form = ProfessorForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect('professor_detail', det_id=prof_id)
    else:
        form = ProfessorForm(instance=professor)
    return render(request, 'professor_update.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def professor_delete(request, prof_id):
    professor = get_object_or_404(Professor, id=prof_id)

    if request.method == 'POST':
        professor.delete()
        return redirect('student_list')

    context = {
        'professor': professor
    }
    return render(request, 'professor_delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def professor_create(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = ProfessorForm(request.POST)

        if form.is_valid():
            # create a new student object from the form data
            professor = form.save()

            # redirect to the student detail page for the new student object
            return redirect('professor_detail', prof_id=professor.pk)
        else:
            # If the form is not valid, print the form errors for debugging
            print(form.errors)
    else:
        # display a blank form
        form = ProfessorForm()

    # render the create student form template with the form instance
    departments = Department.objects.all()
    context = {
                'form': form,
                'departments': departments
            }
    return render(request, 'professor_create.html', context)

@user_passes_test(lambda u: u.is_active)
def request_event_change(request, ev_id):
    event = get_object_or_404(Event, id=ev_id)
    calCouId = event.calendarCourse.id
    calendarCourse = get_object_or_404(CalendarCourse, id=calCouId)
    if request.method == "POST":
        form = CalendarCourseProfForm(request.POST, instance=calendarCourse)
        if form.is_valid():
            if not request.user.is_staff:
                change = Change(
                    room_number = form.cleaned_data['room_number'],
                    start_time = form.cleaned_data['start_time'],
                    end_time = form.cleaned_data['end_time'],
                    date = form.cleaned_data['date'],
                    is_online = form.cleaned_data['is_online'],
                    is_approved = False,
                    is_pending = True,
                    date_created = datetime.now()
                )
                change.save()
                event = get_object_or_404(Event, id=ev_id)
                event.changes.add(change)
                return redirect('event:my_event_list')
    else:
        form = CalendarCourseProfForm(instance=calendarCourse)
        eventDate = event.date
        context={
            'form' : form,
            'eventDate' : eventDate
        }
        return render(request, 'calendarcourse_update.html', context)

def Get_Cal_Courses(request):
    professor = request.user.professor
    calCourses = CalendarCourse.objects.filter(course__professor=professor)
    context = {
        'calendarCourses' : calCourses
    }

    return render(request, 'calendarCourse_list.html', context)
        