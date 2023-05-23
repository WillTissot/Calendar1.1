from django.shortcuts import render, get_object_or_404, redirect
from course.models import Department
from .forms import StudentForm
from .models import Student, EnrolledStudentsOnCourse
from event.models import Event
from course.models import Course, CalendarCourse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta, datetime


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

def update_calendar(request):
    deleteEvents(request)
    createEvents(request)

def deleteEvents(request):
    user= request.user
    events = Event.objects.filter(calendarCourse__course__enrolledstudentsoncourse__student__user_id=user.id).delete()

def createEvents(request):
    student = request.user.student
    enrolledCourses = EnrolledStudentsOnCourse.objects.filter(student=student)
    course_ids = enrolledCourses.values_list('course_id', flat=True)
    calendar_courses = CalendarCourse.objects.filter(id__in=course_ids)
    x = 1

    for calCourse in calendar_courses:
        calSemStartDate = calCourse.calendarSemester.startDate
        day = calCourse.day
        calSemEndDate = calCourse.calendarSemester.endDate
        currentDate = datetime.now().date()

        if currentDate < calSemStartDate:
            x = calSemStartDate.isoweekday()
            timed = timedelta(days=(day - calSemStartDate.isoweekday() + 7) % 7)
            nextEventsStartDate = calSemStartDate + timed
        else:
            creatingEventsStartDate = currentDate + timedelta(days=(day - currentDate.isoweekday() + 7) % 7)

        while nextEventsStartDate <= calSemEndDate:
            newEvent = Event(
            calendarCourse=calCourse,
            created_at= datetime.now(),
            date = nextEventsStartDate
            )
            newEvent.save()
            nextEventsStartDate += timedelta(days=7)
    

    # if request.method == 'POST':
    #     form = EventForm(request.POST)
    #     if form.is_valid():
    #         event = form.save(commit=False)
    #         calendar_course = CalendarCourse.objects.filter(course__enrolled_students=request.user.student).first()
    #         event.calendarCourse = calendar_course
    #         event.full_clean()

    #         current_date = datetime.now().date()
    #         semester_start_date = calendar_course.semester.startDate
    #         semester_end_date = calendar_course.semester.endDate

    #         if current_date < semester_start_date:
    #             week_start_date = semester_start_date
    #         else:
    #             week_start_date = semester_start_date + timedelta(days=(7 - semester_start_date.weekday()))

    #         while week_start_date <= semester_end_date:
    #             new_event = Event(
    #                 calendarCourse=calendar_course,
    #                 start_date=week_start_date,
    #                 end_date=week_start_date + timedelta(days=6)
    #             )
    #             new_event.save()
    #             week_start_date += timedelta(days=7)

    #         return redirect('event_list')  # Redirect to event list or any other page
    # else:
    #     form = EventForm()

    # context = {
    #     'form': form
    # }
    # return render(request, 'create_event.html', context)


