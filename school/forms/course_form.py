from django import forms
from school.models import Courses


class MyDateInput(forms.DateInput):
    """
    由於DateInput的input_type依然為'text'，導致無法html無法呈現我們想要的日期選單效果。
    所以自訂一個widget類，繼承於DateInput，複寫其input_type為'date'即可。
    """
    input_type = 'date'


# 用來新建或修改課程資料
class CoursesCreateXUpdateModelForm(forms.ModelForm):
    start = forms.DateField(label='開始日期', widget=MyDateInput(format='%Y-%m-%d'))
    end = forms.DateField(label='結束日期', widget=MyDateInput(format='%Y-%m-%d'))
    # <input type="date" value="yyyy-mm-dd"> 因為只接受yyyy-mm-dd格式，所以要自行轉換
    comment = forms.CharField(label='課程說明', max_length=512, widget=forms.Textarea)

    class Meta:
        model = Courses
        fields = ['name', 'fee', 'start', 'end', 'limit', 'teacher', 'status', 'comment']

    def __init__(self, *args, my_test=False, **kwargs):
        super().__init__(*args, **kwargs)
        # 為所有的input加入bootstrap的form-control樣式
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if name == 'status':
                field.widget.attrs.update({'class': 'form-check-input'})

