"""
todo: 待處理異常提示文字
request.FILES的資料型態為MultiValueDict，如該表單夾帶多個檔案時，可得到如下模式的資料模式
<MultiValueDict: {'field_name': [<file1>, <file2>, ..., <fileX>]}>
目前Django4.0.2，所提供的FileField在驗證時，其所用的widget(預設為ClearableFileInput),在獲取檔案時是採用.get()方法，導致只能
取得最後一筆檔案。(如上資料，只能取得<fileX>，但如果其可採用.getlist()方法，則可取得[<file1>, <file2>, ..., <fileX>])
如果自行使用request.FILES.getlist()雖可取的所有檔案，但就不能自動驗證，所以
解決方法思路：
1. 修改ClearableFileInput的value_from_datadict()方法，讓其使用.getlist()來取得檔案，再回傳列表形式的檔案供驗證用。
2. 在驗證過程中，FildField裡的.clean()會調用父類的.clean()的方法，其將依序執行
   a. value = self.to_python(value)
   b. self.validate(value)
   c. self.run_validators(value)
   d. return value
   其中，value就是從ClearableFileInput取得的檔案，經處理驗證後，如無異常則回傳，最終會儲存到cleaned_data裡。由於原始設計是
   拿單一檔案去做這些驗證，所以我們的想法是那就用for來循環列表裡的檔案，一個一個交由父類的.clean()去驗證，這樣方可確保列表裡的
   每個檔案都符合驗證規則。

思路參考：
https://stackoverflow.com/questions/46318587/django-uploading-multiple-files-list-of-files-needed-in-cleaned-datafile
"""
from django import forms
from django.forms.widgets import ClearableFileInput, CheckboxInput
from django.core.exceptions import ValidationError


FILE_INPUT_CONTRADICTION = object()


# 自訂widget，可用來取得多檔案(使用.getlist())的ClearableFileInput
class MyMultipleClearableFileInput(ClearableFileInput):
    # override value_from_datadict() method
    def value_from_datadict(self, data, files, name):
        """original code
        upload = super().value_from_datadict(data, files, name)
        其super()為FileInput，故等效
        upload = files.get(name)
        """
        upload = files.getlist(name)  # 改寫使用getlist()

        # 下面這段是當搭配勾選確認框。(加入檔案需取消勾選清除框，或加入檔案維持勾選清除框)
        # 所以我們將upload變成列表並不影響
        if not self.is_required and CheckboxInput().value_from_datadict(
                data, files, self.clear_checkbox_name(name)):

            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # object that FileField will turn into a ValidationError.
                # 請提交一個檔案或確認清除核可項, 不能兩者都做。
                return FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value, as opposed to just None
            return False
        return upload


# 自訂MultipleFileField，配合自訂的widget可處理多個檔案
class MyMultipleFileField(forms.FileField):
    widget = MyMultipleClearableFileInput

    # override clean() method
    def clean(self, data, initial=None):
        # If the widget got contradictory inputs, we raise a validation error
        if data is FILE_INPUT_CONTRADICTION:
            raise ValidationError(self.error_messages['contradiction'], code='contradiction')
        # False means the field value should be cleared; further validation is
        # not needed.
        if data is False:
            if not self.required:
                return False
            # If the field is required, clearing is not possible (the widget
            # shouldn't return False data in that case anyway). False is not
            # in self.empty_value; if a False value makes it this far
            # it should be validated from here on out as None (so it will be
            # caught by the required check).
            data = None
        if not data and initial:
            return initial

        """original code
        return super().clean(data)
        其super()為Field
        驗證過程如無異常，則return傳入的data(從原始碼可看出，其除了驗證外並無對date做其他改變。)
        """
        for each_data in data:
            # 要使用Field的.clean()，因為成功會回傳資料，但我們不需要，所以用 _ 接收。
            _ = super(forms.FileField, self).clean(each_data)
        # 全部驗證成功，則return傳入的data。
        return data

    # override widget_attrs() method。 為widget加入multiple屬性
    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if isinstance(widget, forms.FileInput) and 'multiple' not in widget.attrs:
            attrs.setdefault('multiple', True)
        return attrs


# 自訂MultipleFileField，可配合處理多個圖片檔案。(原理同MyMultipleFileField)
class MyMultipleImageField(forms.ImageField, MyMultipleFileField):
    widget = MyMultipleClearableFileInput

    """使用雙繼承
    同自訂的MyMultipleFileField一樣，也需要自訂可驗證多檔案的clean()方法。
    驗證是否為圖片，是在to_python()方法裡實作，這點繼承forms.ImageField即可;
    而clean()方法，可透過繼承MyMultipleFileField。
    
    __mro__:
    (<'MyMultipleImageField'>, <'ImageField'>, <'MyMultipleFileField'>, <'FileField'>, <'Field'>, <'object'>)
    """

    # override widget_attrs() method。 為widget加入multiple屬性
    """original code
    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if isinstance(widget, FileInput) and 'accept' not in widget.attrs:
            attrs.setdefault('accept', 'image/*')
        return attrs
    """
    def widget_attrs(self, widget):
        attrs = super(forms.ImageField, self).widget_attrs(widget)
        if isinstance(widget, forms.FileInput) and 'accept' not in widget.attrs:
            attrs.setdefault('accept', 'image/*')
        if isinstance(widget, forms.FileInput) and 'multiple' not in widget.attrs:
            attrs.setdefault('multiple', True)
        return attrs
