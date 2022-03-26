"""reference上傳檔案和上傳圖片(僅使用form表單，所以要自行處理上傳的檔案)
參考資料
文件上传：https://docs.djangoproject.com/zh-hans/4.0/topics/http/file-uploads/
将上传的文件绑定到表单中：https://docs.djangoproject.com/zh-hans/4.0/ref/forms/api/#binding-uploaded-files-to-a-form
上传的文件和上传处理程序：https://docs.djangoproject.com/zh-hans/4.0/ref/files/uploads/
"""
from django.shortcuts import render, redirect
from django import forms
from reference.util.upload_form_util import MyMultipleFileField, MyMultipleImageField


"""
************ forms.Form 的檔案上傳
"""


# 如果表格多，也可和views一樣，另外寫forms.py，使用時再import即可
class UploadFileForm(forms.Form):
    name = forms.CharField(label='上傳者名稱', required=False)
    single_file = forms.FileField(label='上傳檔案(單)', required=False)
    # 多檔案使用自訂的MyMultipleFileField
    multiple_file = MyMultipleFileField(label='上傳檔案(多)', max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


# 用來儲存驗證後的檔案
def handle_upload_file(file, path):
    with open(path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        # 注意如果要綁定資料驗證，表單資料在request.POST，而檔案的部分會在request.FILES
        bound_form = UploadFileForm(data=request.POST, files=request.FILES)
        if bound_form.is_valid():
            name = bound_form.cleaned_data['name']

            # 因為使用自訂的MyMultipleFileField，我們可以直接從cleaned_data取得檔案
            single_file = bound_form.cleaned_data['single_file']
            multiple_file = bound_form.cleaned_data['multiple_file']

            folder = r'/Users/chris/OneDrive/Code/pycharm/DjangoNote/static/reference/upload_file/temp/'
            if single_file:
                path = folder+single_file.name
                handle_upload_file(single_file, path)
                print(f'{name}上傳檔案{single_file.name}已儲存至{path}')
            if multiple_file:
                for each_file in multiple_file:
                    path = folder+each_file.name
                    handle_upload_file(each_file, path)
                    print('上傳多檔案：')
                    print(f'{name}上傳檔案{each_file.name}已儲存至{path}')

            return redirect('reference:upload_file')
        else:
            data = {
                'form': bound_form
            }
            return render(request, 'reference/upload/upload_file.html', data)

    data = {
        'form': UploadFileForm()
    }
    return render(request, 'reference/upload/upload_file.html', data)


"""
************ forms.Form 的圖片上傳
"""


class UploadImageForm(forms.Form):
    name = forms.CharField(label='上傳者名稱', required=False)
    single_image = forms.ImageField(label='上傳圖片(單)', required=False)
    # 多圖片使用自訂的MyMultipleImageField
    multiple_image = MyMultipleImageField(label='上傳圖片(多)',
                                          required=False
                                          )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


def upload_image(request):
    if request.method == 'POST':
        bound_form = UploadImageForm(data=request.POST, files=request.FILES)
        if bound_form.is_valid():
            name = bound_form.cleaned_data['name']
            single_image = bound_form.cleaned_data['single_image']
            multiple_image = bound_form.cleaned_data['multiple_image']

            folder = r'/Users/chris/OneDrive/Code/pycharm/DjangoNote/static/reference/upload_file/temp/img/'
            if single_image:
                path = folder + single_image.name
                handle_upload_file(single_image, path)
                print(f'{name}上傳團片{single_image.name}已儲存至{path}')
                print(f'團片{single_image.name}, 尺寸：{single_image.image.width}x{single_image.image.height}')
            if multiple_image:
                for each_file in multiple_image:
                    path = folder + each_file.name
                    handle_upload_file(each_file, path)
                    print(f'{name}上傳檔案{each_file.name}已儲存至{path}')
                    print(f'團片{each_file.name}, 尺寸：{each_file.image.width}x{each_file.image.height}')

            return redirect('reference:upload_image')
        else:
            data = {
                'form': bound_form
            }
            return render(request, 'reference/upload/upload_image.html', data)

    data = {
        'form': UploadImageForm()
    }
    return render(request, 'reference/upload/upload_image.html', data)
