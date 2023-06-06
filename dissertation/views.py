from .forms import DissertationForm, CalendarDissertationForm, DissertationStudentForm
from .models import Dissertation, CalendarDissertation
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

# Create your views here.

# Dissertation CRUD.


@user_passes_test(lambda u: u.is_superuser)
def dissertation_list(request):
    dissertations = Dissertation.objects.all()
    context = {
        'dissertations': dissertations
    }
    return render(request, 'dissertation_list.html', context)

@user_passes_test(lambda u: u.is_superuser)
def dissertation_pending_calendar_event_list(request):
    dissertations_without_calendar = Dissertation.objects.filter(calendardissertation__isnull=True, is_approved=True)
    createCalendarEvent = True
    context = {
        'dissertations': dissertations_without_calendar,
        'createCalendarEvent' : createCalendarEvent
    }
    return render(request, 'dissertation_list.html', context)

def student_dissertation_list(request):
    student = request.user.student
    dissertations = Dissertation.objects.filter(student=student)
    context = { 
        'dissertations': dissertations
    }
    return render(request, 'dissertation_list.html', context)

def dissertation_detail(request, dissertation_id):
    dissertation = get_object_or_404(Dissertation, id=dissertation_id)
    return render(request, 'dissertation_detail.html', {'dissertation': dissertation})

@user_passes_test(lambda u: u.is_superuser)
def dissertation_update(request, dissertation_id):
    dissertation = get_object_or_404(Dissertation, id=dissertation_id)

    if request.method == 'POST':
        form = DissertationForm(request.POST, instance=dissertation)
        if form.is_valid():
            form.save()
            return redirect('dissertation:dissertation_detail', dissertation_id=dissertation_id)
    else:
        form = DissertationForm(instance=dissertation)
    return render(request, 'dissertation_update.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def dissertation_delete(request, dissertation_id):
    dissertation = get_object_or_404(Dissertation, id=dissertation_id)

    if request.method == 'POST':
        dissertation.delete()
        return redirect('dissertation:dissertation_list')

    context = {
        'dissertation': dissertation
    }
    return render(request, 'dissertation_delete.html', context)

def dissertation_create(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            form = DissertationForm(request.POST)
        else:
            form = DissertationStudentForm(request.POST)

        if form.is_valid():
            dissertation = form.save()
            dissertation.student = request.user.student
            dissertation.is_approved = False
            dissertation.save()
            return redirect('dissertation:dissertation_detail', dissertation_id=dissertation.pk)
        else:
            print(form.errors)
    else:

        if request.user.is_superuser:


                form = DissertationForm(request.POST)
        else:
            form = DissertationStudentForm(request.POST)

    context = {
                'form': form
            }
    return render(request, 'dissertation_create.html', context)


# Calendar Dissertation CRUD.


@user_passes_test(lambda u: u.is_superuser)
def calendardissertation_list(request):
    calendardissertations = CalendarDissertation.objects.all()
    context = {
        'calendardissertations': calendardissertations
    }
    return render(request, 'calendardissertation_list.html', context)


def calendardissertation_detail(request, calendardissertation_id):
    calendardissertation = get_object_or_404(CalendarDissertation, id=calendardissertation_id)
    return render(request, 'calendardissertation_detail.html', {'calendardissertation': calendardissertation})

@user_passes_test(lambda u: u.is_superuser)
def calendardissertation_update(request, calendardissertation_id):
    calendardissertation = get_object_or_404(CalendarDissertation, id=calendardissertation_id)

    if request.method == 'POST':
        form = CalendarDissertationForm(request.POST, instance=calendardissertation)
        if form.is_valid():
            form.save()
            return redirect('dissertation:calendardissertation_detail', calendardissertation_id=calendardissertation_id)
    else:
        form = CalendarDissertationForm(instance=calendardissertation)
    return render(request, 'calendardissertation_update.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def calendardissertation_delete(request, calendardissertation_id):
    calendardissertation = get_object_or_404(CalendarDissertation, id=calendardissertation_id)

    if request.method == 'POST':
        calendardissertation.delete()
        return redirect('dissertation:calendardissertation_list')

    context = {
        'calendardissertation': calendardissertation
    }
    return render(request, 'calendardissertation_delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def calendardissertation_create(request):
    if request.method == 'POST':
        form = CalendarDissertationForm(request.POST)

        if form.is_valid():
            calendardissertation = form.save()
            return redirect('dissertation:calendardissertation_detail', calendardissertation_id=calendardissertation.pk)
        else:
            print(form.errors)
    else:
        diss_id = request.GET.get('diss_id')
        if diss_id:
            dissertation = get_object_or_404(Dissertation, id = diss_id)
            initial_values = {
                'dissertation': dissertation
            }
            form = CalendarDissertationForm(dissertation = dissertation)
            isFromDissFlow = True
        else:
            form = CalendarDissertationForm()

    context = {
                'form': form,
                'isFromDissFlow' : isFromDissFlow
            }
    return render(request, 'calendardissertation_create.html', context)
