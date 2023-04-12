from django.shortcuts import get_object_or_404, render

from professor.models import Professor

# Create your views here.

def professor_list(request):
    professors = Professor.objects.all()
    context = {
        'professors': professors
    }
    return render(request, 'professor_list.html', context)

def professor_detail(request, det_id):
    # Retrieve the student object with the provided id
    professor = get_object_or_404(Professor, id=det_id)

    # Render the student detail template with the student object as context
    return render(request, 'professor_detail.html', {'professor': professor})
