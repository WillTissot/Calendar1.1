from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from .forms import SeminarForm, CalendarSeminarForm
from .models import Seminar, CalendarSeminar


# Seminar CRUD.


@user_passes_test(lambda u: u.is_superuser)
def seminar_list(request):
    seminars = Seminar.objects.all()
    context = {
        'seminars': seminars
    }
    return render(request, 'seminar_list.html', context)


def seminar_detail(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id)
    return render(request, 'seminar_detail.html', {'seminar': seminar})

@user_passes_test(lambda u: u.is_superuser)
def seminar_update(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id)

    if request.method == 'POST':
        form = SeminarForm(request.POST, instance=seminar)
        if form.is_valid():
            form.save()
            return redirect('seminar:seminar_detail', seminar_id=seminar_id)
    else:
        form = SeminarForm(instance=seminar)
    return render(request, 'seminar_update.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def seminar_delete(request, seminar_id):
    seminar = get_object_or_404(Seminar, id=seminar_id)

    if request.method == 'POST':
        seminar.delete()
        return redirect('seminar:seminar_list')

    context = {
        'seminar': seminar
    }
    return render(request, 'seminar_delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def seminar_create(request):
    if request.method == 'POST':
        form = SeminarForm(request.POST)

        if form.is_valid():
            seminar = form.save()
            return redirect('seminar:seminar_detail', seminar_id=seminar.pk)
        else:
            print(form.errors)
    else:
        form = SeminarForm()

    context = {
                'form': form
            }
    return render(request, 'seminar_create.html', context)

    
    
# Calendar Seminar CRUD.


@user_passes_test(lambda u: u.is_superuser)
def calendarseminar_list(request):
    calendarseminars = CalendarSeminar.objects.all()
    context = {
        'calendarseminars': calendarseminars
    }
    return render(request, 'calendarseminar_list.html', context)


def calendarseminar_detail(request, calSeminar_id):
    calendarseminar = get_object_or_404(CalendarSeminar, id=calSeminar_id)
    return render(request, 'calendarseminar_detail.html', {'calendarseminar': calendarseminar})

@user_passes_test(lambda u: u.is_superuser)
def calendarseminar_update(request, calSeminar_id):
    calendarseminar = get_object_or_404(CalendarSeminar, id=calSeminar_id)

    if request.method == 'POST':
        form = CalendarSeminarForm(request.POST, instance=calendarseminar)
        if form.is_valid():
            form.save()
            return redirect('seminar:calendarseminar_detail', calSeminar_id=calSeminar_id)
    else:
        form = CalendarSeminarForm(instance=calendarseminar)
    return render(request, 'calendarseminar_update.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def calendarseminar_delete(request, calSeminar_id):
    calendarseminar = get_object_or_404(CalendarSeminar, id=calSeminar_id)
    if request.method == 'POST':
        calendarseminar.delete()
        return redirect('seminar:calendarseminar_list')

    context = {
        'calendarseminar': calendarseminar
    }
    return render(request, 'calendarseminar_delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def calendarseminar_create(request):
    if request.method == 'POST':
        form = CalendarSeminarForm(request.POST)

        if form.is_valid():
            calendarseminar = form.save()
            return redirect('seminar:calendarseminar_detail', calSeminar_id=calendarseminar.pk)
        else:
            print(form.errors)
    else:
        form = CalendarSeminarForm()

    context = {
                'form': form
            }
    return render(request, 'calendarseminar_create.html', context)