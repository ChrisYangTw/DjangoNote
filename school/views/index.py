from django.shortcuts import redirect, render
from school.models import Courses


def index(request):
    data = {
        'courses': Courses.objects.all()
    }
    return render(request, 'school/index.html', data)
