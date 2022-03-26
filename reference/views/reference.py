"""Reference首頁
index:目前用來測試表單設定
"""
from django.shortcuts import render, redirect
from django import forms
from django.forms import widgets
from PIL import Image


class MyDateInput(forms.DateInput):
    """
    由於DateInput的input_type依然為'text'，導致無法html無法呈現我們想要的日期選單效果。
    所以自訂一個widget類，繼承於DateInput，複寫其input_type為'date'即可。
    """
    input_type = 'date'


class TestForms(forms.Form):
    t1 = forms.CharField(
        widget=widgets.TextInput(
            attrs={
                'class': 'testclass',
                'placeholder': '132',
            }
        ),
        label= 'charfield',  # 搭配.label_tag使用，自動生成<label>標籤
        label_suffix='->',  # 搭配.label_tag使用。會與lable拼接。
        initial='abcdefg',  # html的value='abcdefg'
        required=True,  # html的required
        help_text='這是輔助文字',  # 在<input>後，加入<span class="helptext">這是輔助文字</span>
        disabled=False, # html的disabled
        max_length=8,
        min_length=2,
        error_messages={
            'required': '必須輸入',
            'max_length': '太長',
            'min_length': '太短',
        }
    )
    t2 = forms.IntegerField(
        widget=widgets.TextInput,
        max_value=100,
        min_value=0,
        error_messages={
            'max_value': '不可比100大',
            'min_value': '不可比0小',
            'invalid': '需為數字',
        }
    )
    t3 = forms.DateField(widget=MyDateInput)  # 使用自訂的widget


def index(request):
    if request.method == 'GET':
        data = {
            'form': TestForms(),
        }
        return render(request, 'reference/index.html', data)

    # 測試上傳團片
    file = request.FILES.get('f1')
    im = Image.open(file)
    im.show()

    bound_form = TestForms(request.POST)
    if bound_form.is_valid():
        print(f'{bound_form.cleaned_data}')
        return redirect('reference:index')
    else:
        data = {
            'form': bound_form,
        }
        return render(request, 'reference/index.html', data)
