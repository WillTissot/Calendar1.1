from django.shortcuts import get_object_or_404, redirect, render
from course.forms import CourseForm, CalendarSemesterForm
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



#create calendar semesters

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
