"""reference上傳檔案和上傳圖片(僅使用ModeForm，並利用django-cleanup來自動處理移除檔案)
使用form，對上傳的檔案做驗證處理，再使用model來管理檔案的存取。
在管理檔案這部分，當我們從model裡移除一個檔案實例時，存儲在硬碟裡的檔案並不會一併被移除。
解決方式：
todo: 1. 重寫model的delete()方法。
todo: 2. 使用signal dispatcher，設定pre_delete或post_delete
3. 使用第三方模組，django-cleanup。
"""
from django import forms
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from reference.models import Upload


class UploadWithModelForm(forms.ModelForm):
    class Meta:
        model = Upload
        # 可指定要轉成表單字段的模型字段，會依序執行，如要引入全部也可使用 fields = '__all__'
        fields = ['name', 'file', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


def upload_with_model(request):
    if request.method == 'POST':
        bound_form = UploadWithModelForm(data=request.POST, files=request.FILES)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('reference:upload_with_model')
        else:
            data = {
                'form': bound_form
            }
            return render(request, 'reference/upload/upload_with_model.html', data)

    data = {
        'form': UploadWithModelForm(),
        'data': Upload.objects.all()
    }
    return render(request, 'reference/upload/upload_with_model.html', data)


@require_http_methods(['GET'])
def delete_upload_with_model(request, nid):
    try:
        wanted_to_delete_data = Upload.objects.get(id=nid)
    except Upload.DoesNotExist:
        pass
    else:
        wanted_to_delete_data.delete()
    finally:
        return redirect('reference:upload_with_model')
