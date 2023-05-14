from django.shortcuts import get_object_or_404, redirect, render
from course.forms import CourseForm

from course.models import Course, Department
from professor.models import Professor

# Create your views here.

def course_list(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'course_list.html', context)


def course_detail(request, cou_id):
    # Retrieve the student object with the provided id
    course = get_object_or_404(Course, id=cou_id)

    # Render the student detail template with the student object as context
    return render(request, 'course_detail.html', {'course': course})


def course_update(request, cou_id):
    course = get_object_or_404(Course, id=cou_id)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course:course_detail', cou_id=cou_id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_update.html', {'form': form})

def course_delete(request, cou_id):
    course = get_object_or_404(Course, id=cou_id)

    if request.method == 'POST':
        course.delete()
        return redirect('course:course_list')

    context = {
        'course': course
    }
    return render(request, 'course_delete.html', context)


def course_create(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = CourseForm(request.POST)

        if form.is_valid():
            # create a new student object from the form data
            course = form.save()

            # redirect to the student detail page for the new student object
            return redirect('course:course_detail', cou_id=course.pk)
        else:
            # If the form is not valid, print the form errors for debugging
            print(form.errors)
    else:
        # display a blank form
        form = CourseForm()

    # render the create student form template with the form instance
    departments = Department.objects.all()
    professors = Professor.objects.all()
    context = {
                'form': form,
                'departments': departments,
                'professors' : professors
            }
    return render(request, 'course_create.html', context)
