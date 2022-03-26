"""
原本的ClearableFileInput對於給入的initial資料，會渲染成
<a href="{{ widget.value.url }}">{{ widget.value }}</a>
到我們想要點該連結時可以使用另開視窗的方式，所以這裡自訂template，修改其內容為
<a href="{{ widget.value.url }}" target="_blank">{{ widget.value }}</a>
"""

from django.forms import ClearableFileInput


class MyClearableFileInput(ClearableFileInput):
    template_name = "django/forms/widgets/my_add/my_clearable_file_input.html"

# todo: 待研究如何指定自己的資料夾，目前放在django模組的資料夾內
