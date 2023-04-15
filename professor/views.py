from django.shortcuts import get_object_or_404, redirect, render
from course.models import Department
from professor.forms import ProfessorForm

from professor.models import Professor

# Create your views here.

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

def professor_delete(request, prof_id):
    professor = get_object_or_404(Professor, id=prof_id)

    if request.method == 'POST':
        professor.delete()
        return redirect('student_list')

    context = {
        'professor': professor
    }
    return render(request, 'professor_delete.html', context)


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