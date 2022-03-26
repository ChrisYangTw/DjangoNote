from django import forms
from school.models import Teachers
from school.utils.widgets.my_clearable_file_input import MyClearableFileInput


# 用來新建或修改教師資料
class TeacherCreateXUpdateModelForm(forms.ModelForm):
    # 由於希望使用者上傳的圖片名稱小於16個字，但因使用forms.ModelForm來生成表單，且在model裡的ImageField設定
    # max_length=16，其會生成對應的表單來驗證圖片名稱是否小於16個字。然而，在寫入資料庫時，因是會寫入完整的路徑
    # 資料，此時該路徑的長度可能會超出16個字。
    # 所以我們這裡另外寫ImageField表單，並設定max_length。而在model的ImageField字段則不限制。
    photo = forms.ImageField(label='相片', max_length=16, widget=MyClearableFileInput)

    class Meta:
        model = Teachers
        fields = ['name', 'gender', 'photo', 'salary', 'information']
        widgets = {
            'information': forms.Textarea,
        }

    def __init__(self, *args, is_teacher_update=False, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if name == 'name':
                field.widget.attrs.update({'placeholder': '輸入姓名'})
                # 如果是用來編輯表格時，姓名的部分不可改變
                if is_teacher_update:
                    field.widget.attrs.update({'disabled': True})
            if name == 'information':
                field.widget.attrs.update({'placeholder': '撰寫教師介紹'})
