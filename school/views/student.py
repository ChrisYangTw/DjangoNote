"""
學生資訊之CRUD
"""
from django.shortcuts import render, redirect
from django.http import Http404
from school.forms.student_form import StudentCreateXUpdateModelForm
from school.models import Students


def student_list(request):
    # todo: 在中間件中，針對不同層級的使用者，給予不同的level，夾帶到request。方便在渲染時有所區隔。
    data = {
        'level': '1',
        'students': Students.objects.all(),
    }
    return render(request, 'school/student/student_list.html', data)


def student_detail(request):
    try:
        student = Students.objects.get(id=request.GET.get('id'))
        data = {
            'level': '1',
            'student': student
        }
    except Students.DoesNotExist as e:
        raise Http404('查無資料') from e
    return render(request, 'school/student/student_detail.html', data)


def student_create(request):
    if request.method == 'POST':
        bound_form = StudentCreateXUpdateModelForm(data=request.POST, files=request.FILES)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('school:student_list')
        else:
            data = {
                'form': bound_form,
                'call': 'add',
            }
            return render(request, 'school/student/student_create_or_update.html', data)

    data = {
        'form': StudentCreateXUpdateModelForm(),
        'call': 'add',
    }
    return render(request, 'school/student/student_create_or_update.html', data)


def student_update(request):
    try:
        student = Students.objects.get(id=request.GET.get('id'))
    except Students.DoesNotExist:
        return redirect('school:student_list')
    
    if request.method == 'POST':
        bound_form = StudentCreateXUpdateModelForm(data=request.POST, files=request.FILES, instance=student)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('school:student_list')
        else:
            data = {
                'form': bound_form,
                'call': 'update',
            }
            return render(request, 'school/student/student_create_or_update.html', data)

    data = {
        'form': StudentCreateXUpdateModelForm(instance=student),
        'call': 'update',
    }
    return render(request, 'school/student/student_create_or_update.html', data)


def student_delete(request):
    try:
        Students.objects.get(id=request.GET.get('id')).delete()
    except Students.DoesNotExist:
        pass

    return redirect('school:student_list')
