from django.shortcuts import render

from professor.models import Professor

# Create your views here.

def professor_list(request):
    professors = Professor.objects.all()
    context = {
        'professors': professors
    }
    return render(request, 'professor_list.html', context)
