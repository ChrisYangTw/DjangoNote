"""
教師資訊之CRUD
"""
from django.shortcuts import render, redirect
from django.http import Http404
from school.models import Teachers
from school.forms.teacher_form import TeacherCreateXUpdateModelForm


def teacher_list(request):
    # todo: 在中間件中，針對不同層級的使用者，給予不同的level，夾帶到request。方便在渲染時有所區隔。
    data = {
        'level': '1',
        'teachers': Teachers.objects.all()
    }
    return render(request, 'school/teacher/teacher_list.html', data)


def teacher_detail(request):
    try:
        teacher = Teachers.objects.get(id=request.GET.get('id'))
        data = {
            'level': '1',
            'teacher': teacher
        }
    except Teachers.DoesNotExist as e:
        raise Http404('查無資料') from e
    return render(request, 'school/teacher/teacher_detail.html', data)


def teacher_create(request):
    if request.method == 'POST':
        bound_form = TeacherCreateXUpdateModelForm(data=request.POST, files=request.FILES)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('school:teacher_list')
        else:
            data = {
                'form': bound_form,
                'call': 'add'
            }
            return render(request, 'school/teacher/teacher_create_or_update.html', data)

    data = {
        'form': TeacherCreateXUpdateModelForm(),
        'call': 'add',
    }
    return render(request, 'school/teacher/teacher_create_or_update.html', data)


# todo: 透過session設定只有擁有權限者方可進入該頁面
def teacher_update(request):
    try:
        teacher = Teachers.objects.get(id=request.GET.get('id'))
    except Teachers.DoesNotExist:
        return redirect('school:teacher_list')

    if request.method == 'POST':
        # 因為name的<input>設為disabled，且並沒有設定value，所以提交後並會回帶有name的數據，這導致在
        # 驗證時會拋出異常提示。而因為request.POST本身是不可變的，所以使用copy()，取得可變的QueryDict，
        # 以便加入name的資料。
        querydict_data = request.POST.copy()
        querydict_data.setdefault('name', default=teacher.name)

        bound_form = TeacherCreateXUpdateModelForm(data=querydict_data, files=request.FILES, instance=teacher)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('school:teacher_list')
        else:
            data = {
                'form': bound_form,
                'call': 'update'
            }
            return render(request, 'school/teacher/teacher_create_or_update.html', data)

    data = {
        'form': TeacherCreateXUpdateModelForm(instance=teacher, is_teacher_update=True),
        'call': 'update'
    }
    return render(request, 'school/teacher/teacher_create_or_update.html', data)


# todo: 透過session設定只有擁有權限者方可進入該頁面
def teacher_delete(request):
    try:
        Teachers.objects.get(id=request.GET.get('id')).delete()
    except Teachers.DoesNotExist:
        pass

    return redirect('school:teacher_list')
