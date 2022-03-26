from django import forms
from school.models import Students


# 用來新建或修改學生資料
class StudentCreateXUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 為所有的input加入bootstrap的form-control樣式
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
