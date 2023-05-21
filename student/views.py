from django.shortcuts import render, get_object_or_404, redirect
from course.models import Department
from .forms import StudentForm
from .models import Student, EnrolledStudentsOnCourse
from course.models import Course
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

@user_passes_test(lambda u: u.is_superuser)
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

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', det_id=up_id)
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_update.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def student_create(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = StudentForm(request.POST)

        if form.is_valid():
            # create a new student object from the form data
            student = form.save()

            # redirect to the student detail page for the new student object
            return redirect('student:student_detail', det_id=student.pk)
        else:
            # If the form is not valid, print the form errors for debugging
            print(form.errors)
    else:
        # display a blank form
        form = StudentForm()

    # render the create student form template with the form instance
    departments = Department.objects.all()
    context = {
                'form': form,
                'departments': departments
            }
    return render(request, 'student_create.html', context)

@user_passes_test(lambda u: u.is_superuser)
def student_delete(request, del_id):
    student = get_object_or_404(Student, id=del_id)

    if request.method == 'POST':
        student.delete()
        return redirect('student_list')

    context = {
        'student': student
    }
    return render(request, 'student_delete.html', context)


@login_required
def enroll_To_Courses(request):
    _method = request.POST.get('_method')
    if _method == 'POST':
        course_id = request.POST.get('course_id')
        student = request.user.student
        course = get_object_or_404(Course, id=course_id)
        EnrolledStudentsOnCourse.objects.create(student=student, course=course)
        return redirect('student:enroll_to_courses') 
    elif _method == 'DELETE':
        course_id = request.POST.get('course_id')
        student = request.user.student
        course = get_object_or_404(Course, id=course_id)

        enrollment = EnrolledStudentsOnCourse.objects.filter(student=student, course=course).first()
        if enrollment:
            enrollment.delete()

        return redirect('student:enroll_to_courses') 
    else:
        courses = Course.objects.all()
        enrolled_calendarCourses = EnrolledStudentsOnCourse.objects.filter(student=request.user.student)
        enrolled_course_ids = enrolled_calendarCourses.values_list('course_id', flat=True)
        enrolled_courses = courses.filter(id__in=enrolled_course_ids)
        available_courses = courses.exclude(id__in=enrolled_course_ids)

        context = {
            'availableCourses': available_courses,
            'enrolledCourses' : enrolled_courses
        }

        return render(request, 'enroll_to_course.html', context)


