"""
課程資訊之CRUD
"""
from django.shortcuts import render, redirect
from django.http import Http404
from school.models import Courses
from school.forms.course_form import CoursesCreateXUpdateModelForm


def course_list(request):
    # todo: 在中間件中，針對不同層級的使用者，給予不同的level，夾帶到request。方便在渲染時有所區隔。
    data = {
        'level': '1',
        'courses': Courses.objects.all()
    }
    return render(request, 'school/course/course_list.html', data)


def course_detail(request):
    try:
        course = Courses.objects.get(id=request.GET.get('id'))
        data = {
            'level': '1',
            'course': course,
        }
    except Courses.DoesNotExist as e:
        raise Http404('查無資料') from e
    return render(request, 'school/course/course_detail.html', data)


def course_create(request):
    if request.method == 'POST':
        bound_form = CoursesCreateXUpdateModelForm(data=request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('school:course_list')
        else:
            data = {
                'form': bound_form,
                'call': 'add',
            }
            return render(request, 'school/course/course_create_or_update.html', data)

    data = {
        'form': CoursesCreateXUpdateModelForm(),
        'call': 'add',
    }
    return render(request, 'school/course/course_create_or_update.html', data)


def course_update(request):
    try:
        course = Courses.objects.get(id=request.GET.get('id'))
    except Courses.DoesNotExist:
        return redirect('school:course_list')

    if request.method == 'POST':
        bound_form = CoursesCreateXUpdateModelForm(data=request.POST, files=request.FILES, instance=course)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('school:course_list')
        else:
            data = {
                'form': bound_form,
                'call': 'update',
            }
            return render(request, 'school/course/course_create_or_update.html', data)

    data = {
        'form': CoursesCreateXUpdateModelForm(instance=course),
        'call': 'update',
    }
    return render(request, 'school/course/course_create_or_update.html', data)


def course_delete(request):
    try:
        Courses.objects.get(id=request.GET.get('id')).delete()
    except Courses.DoesNotExist:
        pass

    return redirect('school:course_list')
