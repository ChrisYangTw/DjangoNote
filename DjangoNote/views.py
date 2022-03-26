"""DjangoNote
index:首頁
test:測試用
"""
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'DjangoNote/index.html')


def test(request):
    attrs = [attr for attr in dir(request) if not attr.startswith('__')]
    for attr in attrs:
        attr_or_method = getattr(request, attr)
        if callable(attr_or_method) and \
                attr not in ['_get_full_path', '_set_content_type_params', '_set_post', 'accepts',
                             'get_signed_cookie', 'parse_file_upload']:
            print(f'{attr}, {attr_or_method()}')
        else:
            print(f'{attr}, {attr_or_method}')
    return HttpResponse('456')
