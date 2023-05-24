from django.shortcuts import get_object_or_404, redirect, render
from course.forms import CourseForm, CalendarSemesterForm, CalendarCourseForm, SemesterForm
from course.models import Course, Department, CalendarCourse, Semester, CalendarSemester
from professor.models import Professor
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

@user_passes_test(lambda u: u.is_superuser)
def course_list(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'course_list.html', context)


def course_detail(request, cou_id):
    course = get_object_or_404(Course, id=cou_id)
    return render(request, 'course_detail.html', {'course': course})

@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
def course_delete(request, cou_id):
    course = get_object_or_404(Course, id=cou_id)

    if request.method == 'POST':
        course.delete()
        return redirect('course:course_list')

    context = {
        'course': course
    }
    return render(request, 'course_delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            course = form.save()
            return redirect('course:course_detail', cou_id=course.pk)
        else:
            print(form.errors)
    else:
        form = CourseForm()

    departments = Department.objects.all()
    professors = Professor.objects.all()
    context = {
                'form': form,
                'departments': departments,
                'professors' : professors
            }
    return render(request, 'course_create.html', context)

#calendar course CRUD

@user_passes_test(lambda u: u.is_superuser)
def calendarcourse_list(request):
    calendarCourses = CalendarCourse.objects.all()
    context = {
        'calendarCourses': calendarCourses
    }
    return render(request, 'calendarCourse_list.html', context)

def calendarcourse_detail(request, cal_id):
    calendarCourse = get_object_or_404(CalendarCourse, id=cal_id)
    return render(request, 'calendarCourse_detail.html', {'calendarCourse': calendarCourse})

@user_passes_test(lambda u: u.is_superuser)
def calendarcourse_update(request, cal_id):
    calendarCourse = get_object_or_404(CalendarCourse, id=cal_id)

    if request.method == 'POST':
        form = CalendarCourseForm(request.POST, instance=calendarCourse)
        if form.is_valid():
            form.save()
            return redirect('course:calendarcourse_detail', cal_id=cal_id)
    else:
        form = CalendarCourseForm(instance=calendarCourse)
    return render(request, 'calendarcourse_update.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def calendarcourse_create(request):
    if request.method == 'POST':
        form = CalendarCourseForm(request.POST)

        if form.is_valid():
            calendarCourse = form.save()
            return redirect('course:calendarcourse_detail', cal_id=calendarCourse.pk)
        else:
            print(form.errors)
    else:
        form = CalendarCourseForm()

    context = {
                'form': form
            }
    return render(request, 'calendarCourse_create.html', context)

@user_passes_test(lambda u: u.is_superuser)
def calendarcourse_delete(request, cal_id):
    calCourse = get_object_or_404(CalendarCourse, id=cal_id)

    if request.method == 'POST':
        calCourse.delete()
        return redirect('course:calendarcourse_list')

    context = {
        'calendarCourse': calCourse
    }
    return render(request, 'calendarCourse_delete.html', context)


#semester CRUD

@user_passes_test(lambda u: u.is_superuser)
def semester_list(request):
    semesters = Semester.objects.all()
    context = {
        'semesters': semesters
    }
    return render(request, 'semester_list.html', context)

def semester_detail(request, sem_id):
    semester = get_object_or_404(Semester, id=sem_id)
    return render(request, 'semester_detail.html', {'semester': semester})

@user_passes_test(lambda u: u.is_superuser)
def semester_update(request, sem_id):
    semester = get_object_or_404(Semester, id=sem_id)

    if request.method == 'POST':
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            return redirect('course:semester_detail', sem_id=sem_id)
    else:
        form = SemesterForm(instance=semester)
    return render(request, 'semester_update.html', {'form': form})

def semester_create(request):
    if request.method == 'POST':
        form = SemesterForm(request.POST)

        if form.is_valid():
            semester = form.save()
            return redirect('course:semester_detail', sem_id=semester.pk)
        else:
            print(form.errors)
    else:
        form = SemesterForm()

    context = {
                'form': form
            }
    return render(request, 'semester_create.html', context)

@user_passes_test(lambda u: u.is_superuser)
def semester_delete(request, sem_id):
    semester = get_object_or_404(Semester, id=sem_id)

    if request.method == 'POST':
        semester.delete()
        return redirect('course:semester_list')

    context = {
        'semester': semester
    }
    return render(request, 'semester_delete.html', context)


#calendar semesters CRUD

@user_passes_test(lambda u: u.is_superuser)
def calendarsemester_list(request):
    calendarSemesters = CalendarSemester.objects.all()
    context = {
        'calendarSemesters': calendarSemesters
    }
    return render(request, 'calendarSemester_list.html', context)

def calendarsemester_detail(request, sem_id):
    calendarSemester = get_object_or_404(CalendarSemester, id=sem_id)
    return render(request, 'calendarSemester_detail.html', {'calendarSemester': calendarSemester})

@user_passes_test(lambda u: u.is_superuser)
def calendarsemester_update(request, sem_id):
    calendarSemester = get_object_or_404(CalendarSemester, id=sem_id)

    if request.method == 'POST':
        form = CalendarSemesterForm(request.POST, instance=calendarSemester)
        if form.is_valid():
            form.save()
            return redirect('course:calendarSemester_detail', sem_id=sem_id)
    else:
        form = CalendarSemesterForm(instance=calendarSemester)
    return render(request, 'calendarSemester_update.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def calendarsemester_create(request):
    if request.method == 'POST':
        form = CalendarSemesterForm(request.POST)

        if form.is_valid():
            calendarSemester = form.save()
            return redirect('course:calendarSemester_detail', sem_id=calendarSemester.pk)
        else:
            print(form.errors)
    else:
        form = CalendarSemesterForm()

    semesters = Semester.objects.all()
    context = {
                'form': form,
                'semesters': semesters
            }
    return render(request, 'calendarSemester_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def calendarsemester_delete(request, sem_id):
    calSemester = get_object_or_404(CalendarSemester, id=sem_id)

    if request.method == 'POST':
        calSemester.delete()
        return redirect('course:calendarSemester_list')

    context = {
        'calendarSemester': calSemester
    }
    return render(request, 'calendarSemester_delete.html', context)
