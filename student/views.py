from django.shortcuts import render, get_object_or_404, redirect
from .forms import StudentForm
from .models import Student


def student_list(request):
    students = Student.objects.all()
    context = {
        'students': students
    }
    return render(request, 'student_list.html', context)


def student_detail(request, det_id):
    # Retrieve the student object with the provided id
    student = get_object_or_404(Student, id=det_id)

    # Render the student detail template with the student object as context
    return render(request, 'student_detail.html', {'student': student})


def student_update(request, up_id):
    student = get_object_or_404(Student, id=up_id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_detail', det_id=up_id)
    return render(request, 'student_update.html', {'form': form})


def student_create(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = StudentForm(request.POST)

        if form.is_valid():
            # create a new student object from the form data
            student = form.save()

            # redirect to the student detail page for the new student object
            return redirect('student_detail', det_id=student.pk)
    else:
        # display a blank form
        form = StudentForm()

    # render the create student form template with the form instance
    context = {'form': form}
    return render(request, 'student_create.html', context)


def student_delete(request, del_id):
    student = get_object_or_404(Student, id=del_id)

    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    context = {
        'student': student
    }
    return render(request, 'student_delete.html', context)
